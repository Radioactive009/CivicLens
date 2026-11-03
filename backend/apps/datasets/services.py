import io
import json
import pandas as pd
from django.utils import timezone
from django.db import transaction
from .models import Dataset, DatasetImportJob
from apps.constituencies.models import State, District, Constituency
from apps.elections.models import PoliticalParty, Candidate, Election, ElectionResult
from apps.demographics.models import DemographicIndicator, DataSource

def process_dataset_file(dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
    except Dataset.DoesNotExist:
        return False, "Dataset not found"

    job = DatasetImportJob.objects.create(
        dataset=dataset,
        status=DatasetImportJob.Status.PROCESSING
    )
    dataset.processing_status = Dataset.ProcessingStatus.PROCESSING
    dataset.save()

    error_log = []
    successful = 0
    failed = 0

    try:
        file_path = dataset.file.path
        if dataset.file_type == 'csv' or file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif dataset.file_type in ['xlsx', 'xls'] or file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        elif dataset.file_type == 'json' or file_path.endswith('.json'):
            df = pd.read_json(file_path)
        else:
            df = pd.read_csv(file_path)

        total_rows = len(df)
        dataset.row_count = total_rows

        if dataset.dataset_type == Dataset.DatasetType.CONSTITUENCIES:
            # Expected columns: state_name, state_code, district_name, district_code, constituency_name, constituency_code, constituency_type, lat, lon
            for index, row in df.iterrows():
                try:
                    with transaction.atomic():
                        state_name = str(row.get('state_name', 'Haryana')).strip()
                        state_code = str(row.get('state_code', 'HR')).strip().upper()
                        state, _ = State.objects.get_or_create(
                            state_code=state_code,
                            defaults={'name': state_name}
                        )

                        dist_name = str(row.get('district_name', '')).strip()
                        dist_code = str(row.get('district_code', f"{state_code}_{dist_name.upper()}")).strip()
                        district = None
                        if dist_name:
                            district, _ = District.objects.get_or_create(
                                district_code=dist_code,
                                defaults={'name': dist_name, 'state': state}
                            )

                        const_code = str(row.get('constituency_code', '')).strip()
                        const_name = str(row.get('constituency_name', '')).strip()
                        c_type = str(row.get('constituency_type', 'AC')).strip().upper()
                        lat = float(row.get('latitude', 0)) if pd.notna(row.get('latitude')) else None
                        lon = float(row.get('longitude', 0)) if pd.notna(row.get('longitude')) else None

                        if not const_code or not const_name:
                            raise ValueError("Missing constituency_code or constituency_name")

                        Constituency.objects.update_or_create(
                            constituency_code=const_code,
                            defaults={
                                'name': const_name,
                                'state': state,
                                'district': district,
                                'constituency_type': c_type,
                                'latitude': lat,
                                'longitude': lon,
                            }
                        )
                        successful += 1
                except Exception as row_err:
                    failed += 1
                    error_log.append(f"Row {index + 1}: {str(row_err)}")

        elif dataset.dataset_type == Dataset.DatasetType.DEMOGRAPHICS:
            # Expected columns: name, category, region_type, region_identifier, region_name, value, unit, reference_year
            for index, row in df.iterrows():
                try:
                    with transaction.atomic():
                        ind_name = str(row.get('name', '')).strip()
                        category = str(row.get('category', 'DEMOGRAPHICS')).strip().upper()
                        r_type = str(row.get('region_type', 'CONSTITUENCY')).strip().upper()
                        r_id = str(row.get('region_identifier', '')).strip()
                        r_name = str(row.get('region_name', '')).strip()
                        val = float(row.get('value', 0))
                        unit = str(row.get('unit', 'Count')).strip()
                        ref_year = int(row.get('reference_year', dataset.reference_year or 2024))

                        if not ind_name or not r_id:
                            raise ValueError("Missing name or region_identifier")

                        DemographicIndicator.objects.update_or_create(
                            name=ind_name,
                            region_identifier=r_id,
                            reference_year=ref_year,
                            defaults={
                                'category': category,
                                'region_type': r_type,
                                'region_name': r_name,
                                'value': val,
                                'unit': unit,
                                'source': dataset.source,
                            }
                        )
                        successful += 1
                except Exception as row_err:
                    failed += 1
                    error_log.append(f"Row {index + 1}: {str(row_err)}")

        elif dataset.dataset_type == Dataset.DatasetType.ELECTIONS:
            # Expected columns: constituency_code, election_year, election_type, candidate_name, party_name, party_abbrev, votes_received, position, total_votes_polled, total_electors
            for index, row in df.iterrows():
                try:
                    with transaction.atomic():
                        c_code = str(row.get('constituency_code', '')).strip()
                        year = int(row.get('election_year', 2024))
                        e_type = str(row.get('election_type', 'VIDHAN_SABHA')).strip().upper()
                        cand_name = str(row.get('candidate_name', '')).strip()
                        party_name = str(row.get('party_name', 'Independent')).strip()
                        party_abbr = str(row.get('party_abbreviation', 'IND')).strip().upper()
                        votes = int(row.get('votes_received', 0))
                        pos = int(row.get('position', 1))
                        total_valid = int(row.get('total_valid_votes', votes))
                        polled = int(row.get('total_votes_polled', total_valid))
                        electors = int(row.get('total_electors', int(polled * 1.35) if polled else 100000))

                        constituency = Constituency.objects.get(constituency_code=c_code)
                        turnout = round((polled / electors * 100) if electors > 0 else 0, 2)

                        election, _ = Election.objects.get_or_create(
                            election_year=year,
                            election_type=e_type,
                            constituency=constituency,
                            defaults={
                                'election_name': f"{constituency.name} General Election {year}",
                                'state': constituency.state,
                                'total_electors': electors,
                                'total_votes_polled': polled,
                                'turnout_percentage': turnout,
                            }
                        )

                        party, _ = PoliticalParty.objects.get_or_create(
                            abbreviation=party_abbr,
                            defaults={'name': party_name}
                        )

                        candidate, _ = Candidate.objects.get_or_create(
                            name=cand_name,
                            party=party
                        )

                        vote_share = round((votes / total_valid * 100) if total_valid > 0 else 0, 2)

                        ElectionResult.objects.update_or_create(
                            election=election,
                            candidate=candidate,
                            defaults={
                                'votes_received': votes,
                                'vote_share': vote_share,
                                'position': pos,
                                'total_valid_votes': total_valid
                            }
                        )
                        successful += 1
                except Exception as row_err:
                    failed += 1
                    error_log.append(f"Row {index + 1}: {str(row_err)}")

        job.status = DatasetImportJob.Status.COMPLETED if failed == 0 else (DatasetImportJob.Status.COMPLETED if successful > 0 else DatasetImportJob.Status.FAILED)
        job.total_records = total_rows
        job.successful_records = successful
        job.failed_records = failed
        job.error_log = error_log[:100]  # Store up to 100 errors
        job.completed_at = timezone.now()
        job.save()

        dataset.processing_status = Dataset.ProcessingStatus.COMPLETED if successful > 0 else Dataset.ProcessingStatus.FAILED
        dataset.validation_summary = {
            'total_rows': total_rows,
            'imported': successful,
            'rejected': failed,
            'sample_errors': error_log[:5]
        }
        dataset.save()
        return True, f"Imported {successful} rows successfully. {failed} failed."

    except Exception as e:
        job.status = DatasetImportJob.Status.FAILED
        job.error_log = [str(e)]
        job.completed_at = timezone.now()
        job.save()

        dataset.processing_status = Dataset.ProcessingStatus.FAILED
        dataset.validation_summary = {'error': str(e)}
        dataset.save()
        return False, str(e)

