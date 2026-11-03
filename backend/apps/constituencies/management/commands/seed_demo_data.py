import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.constituencies.models import State, District, Constituency
from apps.elections.models import PoliticalParty, Candidate, Election, ElectionResult
from apps.demographics.models import DataSource, DemographicIndicator
from apps.intelligence.models import NewsArticle
from apps.datasets.models import Dataset

User = get_user_model()

HARYANA_DISTRICTS = [
    ("Ambala", "AMB", 30.3782, 76.7767),
    ("Bhiwani", "BHI", 28.7830, 76.1397),
    ("Charkhi Dadri", "CDA", 28.5921, 76.2653),
    ("Faridabad", "FAR", 28.4089, 77.3178),
    ("Fatehabad", "FAT", 29.5152, 75.4554),
    ("Gurugram", "GUR", 28.4595, 77.0266),
    ("Hisar", "HIS", 29.1492, 75.7217),
    ("Jhajjar", "JHJ", 28.6063, 76.6565),
    ("Jind", "JIN", 29.3140, 76.3146),
    ("Kaithal", "KAI", 29.8015, 76.3996),
    ("Karnal", "KAR", 29.6857, 76.9905),
    ("Kurukshetra", "KUR", 29.9695, 76.8783),
    ("Mahendragarh", "MAH", 28.2796, 76.1517),
    ("Nuh", "NUH", 28.1090, 77.0142),
    ("Palwal", "PAL", 28.1487, 77.3320),
    ("Panchkula", "PAN", 30.6942, 76.8606),
    ("Panipat", "PNP", 29.3909, 76.9635),
    ("Rewari", "REW", 28.1828, 76.6186),
    ("Rohtak", "ROH", 28.8955, 76.6066),
    ("Sirsa", "SIR", 29.5349, 75.0289),
    ("Sonipat", "SON", 28.9931, 77.0151),
    ("Yamunanagar", "YAM", 30.1290, 77.2674)
]

# 24 representative Vidhan Sabha constituencies across Haryana
CONSTITUENCIES_DATA = [
    ("Kalka", "HR-AC-01", "Panchkula", "GEN", 30.8344, 76.9348),
    ("Panchkula", "HR-AC-02", "Panchkula", "GEN", 30.6942, 76.8606),
    ("Naraingarh", "HR-AC-03", "Ambala", "GEN", 30.4789, 77.1287),
    ("Ambala Cantt", "HR-AC-04", "Ambala", "GEN", 30.3475, 76.8406),
    ("Ambala City", "HR-AC-05", "Ambala", "GEN", 30.3782, 76.7767),
    ("Jagadhri", "HR-AC-07", "Yamunanagar", "GEN", 30.1727, 77.2986),
    ("Yamunanagar", "HR-AC-08", "Yamunanagar", "GEN", 30.1290, 77.2674),
    ("Thanesar", "HR-AC-12", "Kurukshetra", "GEN", 29.9790, 76.8200),
    ("Kaithal", "HR-AC-17", "Kaithal", "GEN", 29.8015, 76.3996),
    ("Karnal", "HR-AC-21", "Karnal", "GEN", 29.6857, 76.9905),
    ("Gharaunda", "HR-AC-23", "Karnal", "GEN", 29.5385, 76.9712),
    ("Panipat City", "HR-AC-25", "Panipat", "GEN", 29.3909, 76.9635),
    ("Sonipat", "HR-AC-31", "Sonipat", "GEN", 28.9931, 77.0151),
    ("Rai", "HR-AC-32", "Sonipat", "GEN", 28.9272, 77.0988),
    ("Jind", "HR-AC-36", "Jind", "GEN", 29.3140, 76.3146),
    ("Uchana Kalan", "HR-AC-37", "Jind", "GEN", 29.4673, 76.1772),
    ("Hisar", "HR-AC-52", "Hisar", "GEN", 29.1492, 75.7217),
    ("Adampur", "HR-AC-47", "Hisar", "GEN", 29.2785, 75.4675),
    ("Rohtak", "HR-AC-62", "Rohtak", "GEN", 28.8955, 76.6066),
    ("Garhi Sampla-Kiloi", "HR-AC-61", "Rohtak", "GEN", 28.8078, 76.7681),
    ("Badli", "HR-AC-65", "Jhajjar", "GEN", 28.5835, 76.8115),
    ("Gurgaon", "HR-AC-77", "Gurugram", "GEN", 28.4595, 77.0266),
    ("Badshahpur", "HR-AC-76", "Gurugram", "GEN", 28.3902, 77.0583),
    ("Faridabad", "HR-AC-89", "Faridabad", "GEN", 28.4089, 77.3178),
]

PARTIES_DATA = [
    ("Bharatiya Janata Party", "BJP", "BJP", "#F97316", "National political party"),
    ("Indian National Congress", "INC", "INC", "#3B82F6", "National political party"),
    ("Indian National Lok Dal", "INLD", "INLD", "#10B981", "Regional political party"),
    ("Jannayak Janta Party", "JJP", "JJP", "#EC4899", "Regional political party"),
    ("Aam Aadmi Party", "AAP", "AAP", "#06B6D4", "National political party"),
    ("Independent", "IND", "IND", "#64748B", "Independent candidate"),
]

class Command(BaseCommand):
    help = 'Seeds initial demonstration records for Haryana state, constituencies, elections, and indicators.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Beginning CivicLens database seeding..."))

        # 1. Default Users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@civiclens.org',
                'first_name': 'Chief',
                'last_name': 'Administrator',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('Admin@12345')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / Admin@12345)"))

        analyst_user, created = User.objects.get_or_create(
            username='analyst',
            defaults={
                'email': 'analyst@civiclens.org',
                'first_name': 'Research',
                'last_name': 'Analyst',
                'role': User.Role.ANALYST,
            }
        )
        if created:
            analyst_user.set_password('Analyst@12345')
            analyst_user.save()
            self.stdout.write(self.style.SUCCESS("Created analyst user (analyst / Analyst@12345)"))

        # 2. State
        haryana, _ = State.objects.get_or_create(
            state_code='HR',
            defaults={
                'name': 'Haryana',
                'capital': 'Chandigarh',
                'latitude': 29.0588,
                'longitude': 76.0856,
            }
        )

        # 3. Districts
        district_objs = {}
        for d_name, d_code, lat, lon in HARYANA_DISTRICTS:
            dist, _ = District.objects.get_or_create(
                district_code=f"HR_{d_code}",
                defaults={
                    'name': d_name,
                    'state': haryana,
                    'headquarters': d_name,
                    'latitude': lat,
                    'longitude': lon,
                }
            )
            district_objs[d_name] = dist

        # 4. Constituencies
        constituency_objs = {}
        for c_name, c_code, dist_name, res, lat, lon in CONSTITUENCIES_DATA:
            dist = district_objs.get(dist_name)
            const, _ = Constituency.objects.get_or_create(
                constituency_code=c_code,
                defaults={
                    'name': c_name,
                    'state': haryana,
                    'district': dist,
                    'constituency_type': Constituency.ConstituencyType.ASSEMBLY,
                    'is_reserved': res,
                    'latitude': lat,
                    'longitude': lon,
                    'boundary_reference': f"ECI-DELIM-HR-{c_code}",
                }
            )
            constituency_objs[c_name] = const

        # 5. Political Parties
        party_objs = {}
        for p_name, p_abbr, p_code, p_color, p_desc in PARTIES_DATA:
            party, _ = PoliticalParty.objects.get_or_create(
                abbreviation=p_abbr,
                defaults={
                    'name': p_name,
                    'party_code': p_code,
                    'color_hex': p_color,
                    'description': p_desc
                }
            )
            party_objs[p_abbr] = party

        # 6. Data Source
        datasource_eci, _ = DataSource.objects.get_or_create(
            source_name='Election Commission of India (ECI)',
            defaults={
                'source_url': 'https://results.eci.gov.in',
                'source_type': 'Official Election Portal',
                'license_information': 'Open Government Data (OGD) Platform India',
                'description': 'Official gazette releases and election statistical reports.'
            }
        )

        datasource_census, _ = DataSource.objects.get_or_create(
            source_name='Directorate of Economics and Statistics, Haryana',
            defaults={
                'source_url': 'https://esaharyana.gov.in',
                'source_type': 'State Statistical Directorate',
                'license_information': 'Government Open Data Portal',
                'description': 'District statistical handbooks and demographic digests.'
            }
        )

        # 7. Elections (2019 and 2024 Assembly Elections)
        random.seed(42)
        candidates_cache = {}

        for year in [2019, 2024]:
            for const_name, const in constituency_objs.items():
                total_electors = random.randint(140000, 240000)
                turnout_pct = round(random.uniform(62.5, 78.5), 2)
                polled_votes = int(total_electors * (turnout_pct / 100.0))

                election, _ = Election.objects.get_or_create(
                    election_year=year,
                    election_type=Election.ElectionType.ASSEMBLY,
                    constituency=const,
                    defaults={
                        'election_name': f"Haryana Legislative Assembly Election {year}",
                        'state': haryana,
                        'total_electors': total_electors,
                        'total_votes_polled': polled_votes,
                        'turnout_percentage': turnout_pct,
                        'data_source': 'Election Commission of India (ECI)',
                    }
                )

                # Generate candidates and results
                parties = ['BJP', 'INC', 'INLD', 'JJP', 'AAP', 'IND']
                # Determine winner
                if year == 2024:
                    winner_party = random.choice(['BJP', 'INC', 'BJP', 'INC', 'INLD'])
                else:
                    winner_party = random.choice(['BJP', 'INC', 'JJP', 'INLD'])

                parties_ordered = [winner_party] + [p for p in parties if p != winner_party]

                winner_share = round(random.uniform(41.0, 52.0), 2)
                runner_up_share = round(winner_share - random.uniform(2.5, 9.0), 2)
                third_share = round(random.uniform(8.0, 15.0), 2)
                fourth_share = round(random.uniform(3.0, 8.0), 2)
                remaining = max(1.0, round(100.0 - (winner_share + runner_up_share + third_share + fourth_share), 2))
                ind_share = round(remaining, 2)

                shares = [winner_share, runner_up_share, third_share, fourth_share, ind_share]

                for pos, (p_abbr, share) in enumerate(zip(parties_ordered[:5], shares), start=1):
                    cand_name = f"{const_name} Candidate {p_abbr} ({year})"
                    party = party_objs.get(p_abbr)
                    cand_key = f"{cand_name}_{p_abbr}"

                    if cand_key not in candidates_cache:
                        cand, _ = Candidate.objects.get_or_create(
                            name=cand_name,
                            party=party,
                            defaults={'candidate_reference': f"ECI-CAND-{cand_name.replace(' ', '_')}"}
                        )
                        candidates_cache[cand_key] = cand
                    else:
                        cand = candidates_cache[cand_key]

                    cand_votes = int(polled_votes * (share / 100.0))

                    ElectionResult.objects.update_or_create(
                        election=election,
                        candidate=cand,
                        defaults={
                            'votes_received': cand_votes,
                            'vote_share': share,
                            'position': pos,
                            'total_valid_votes': polled_votes,
                        }
                    )

        # 8. Demographic Indicators
        indicators_def = [
            ("Total Population", "DEMOGRAPHICS", "Count", (170000, 320000)),
            ("Literacy Rate", "LITERACY", "%", (72.4, 88.6)),
            ("Female Literacy Rate", "LITERACY", "%", (65.2, 82.3)),
            ("Workforce Participation Rate", "EMPLOYMENT", "%", (38.5, 52.4)),
            ("Primary Health Centres", "HEALTHCARE", "Count", (4, 14)),
            ("Electrified Households Ratio", "INFRASTRUCTURE", "%", (97.5, 99.8)),
            ("Piped Drinking Water Access", "INFRASTRUCTURE", "%", (82.0, 96.5)),
            ("Agricultural Land Share", "SOCIOECONOMIC", "%", (55.0, 84.0)),
        ]

        for const_name, const in constituency_objs.items():
            for ref_year in [2021, 2024]:
                for ind_name, cat, unit, val_range in indicators_def:
                    val = round(random.uniform(val_range[0], val_range[1]), 1) if unit == '%' else int(random.uniform(val_range[0], val_range[1]))
                    DemographicIndicator.objects.update_or_create(
                        name=ind_name,
                        region_identifier=const.constituency_code,
                        reference_year=ref_year,
                        defaults={
                            'category': cat,
                            'region_type': DemographicIndicator.RegionType.CONSTITUENCY,
                            'region_name': const.name,
                            'value': float(val),
                            'unit': unit,
                            'source': datasource_census,
                            'methodology': 'District Statistical Handbook and Census Statistical Survey'
                        }
                    )

        # 9. Public Issue Intelligence Articles
        articles_data = [
            ("Panipat Industrial Corridor Phase II Cleared with New Water Treatment Plant", "Panipat", "INFRASTRUCTURE", "POSITIVE", 0.75, ["panipat", "industry", "water", "infrastructure"]),
            ("Farmers at Kurukshetra Mandi Request Faster Paddy Procurement Logistics", "Kurukshetra", "AGRICULTURE", "CONCERN", -0.45, ["kurukshetra", "mandi", "farmer", "paddy", "procurement"]),
            ("Gurugram Metro Extension Project Secures Key Environmental Clearances", "Gurugram", "TRANSPORTATION", "POSITIVE", 0.82, ["gurugram", "metro", "transport", "project"]),
            ("Air Quality Index in Faridabad and Sonipat Enters Severe Category as Winter Stubble Fires Rise", "Faridabad", "ENVIRONMENT", "CONCERN", -0.78, ["faridabad", "aqi", "pollution", "stubble"]),
            ("New Civil Hospital Wing Inaugurated in Ambala Cantt Expanding Specialized Pediatric Care", "Ambala", "HEALTHCARE", "POSITIVE", 0.85, ["ambala", "hospital", "healthcare", "pediatric"]),
            ("Hisar Agricultural University Introduces Climate-Resilient High-Yield Wheat Strain", "Hisar", "AGRICULTURE", "POSITIVE", 0.68, ["hisar", "agriculture", "wheat", "crop"]),
            ("Youth Skill Development Centers Launched Across Karnal and Kaithal to Boost Manufacturing Jobs", "Karnal", "EMPLOYMENT", "POSITIVE", 0.70, ["karnal", "kaithal", "jobs", "employment", "skills"]),
            ("Residents of Badli and Jhajjar Rural Areas Submit Memorandums Demanding Road Repairs", "Jhajjar", "INFRASTRUCTURE", "CONCERN", -0.38, ["jhajjar", "road", "infrastructure", "complaint"]),
            ("State Government Digitizes Ration Distribution with Biometric Portals in Rohtak", "Rohtak", "PUBLIC_SERVICES", "POSITIVE", 0.55, ["rohtak", "ration", "portal", "governance"]),
            ("Sonipat Industrial Belt Sees Expansion as 14 New Manufacturing Units Begin Setup", "Sonipat", "EMPLOYMENT", "POSITIVE", 0.72, ["sonipat", "manufacturing", "industry", "jobs"]),
            ("Drainage Upgrades Announced for Low-Lying Urban Localities in Panchkula Ahead of Monsoons", "Panchkula", "INFRASTRUCTURE", "NEUTRAL", 0.15, ["panchkula", "drainage", "infrastructure", "municipal"]),
            ("Health Directorate Deploys Mobile Medical Units Across Nuh and Mewat Region", "Nuh", "HEALTHCARE", "POSITIVE", 0.64, ["nuh", "health", "medical", "clinic"]),
        ]

        for idx, (title, geo, cat, sent_label, sent_score, kw) in enumerate(articles_data, 1):
            NewsArticle.objects.update_or_create(
                article_url=f"https://regional-news.civiclens.org/haryana/articles/2024/{idx}",
                defaults={
                    'title': title,
                    'description': f"Analytical summary of public-interest development regarding {title.lower()}.",
                    'content': f"Detailed reporting on civic services, public indicators, and governmental initiatives in {geo}.",
                    'source_name': 'Haryana Civic Herald',
                    'published_at': timezone.now() - timezone.timedelta(days=idx * 2),
                    'category': cat,
                    'sentiment_label': sent_label,
                    'sentiment_score': sent_score,
                    'geographic_reference': geo,
                    'keywords': kw,
                }
            )

        # 10. Sample Dataset Record
        Dataset.objects.get_or_create(
            dataset_name='Haryana Assembly Elections 2024 Official Returns',
            defaults={
                'dataset_type': Dataset.DatasetType.ELECTIONS,
                'source': datasource_eci,
                'file_name': 'haryana_assembly_2024_official.csv',
                'file_type': 'csv',
                'geographical_coverage': 'Haryana, India',
                'reference_year': 2024,
                'processing_status': Dataset.ProcessingStatus.COMPLETED,
                'uploaded_by': admin_user,
                'row_count': 90,
                'validation_summary': {'total_rows': 90, 'imported': 90, 'rejected': 0}
            }
        )

        self.stdout.write(self.style.SUCCESS("CivicLens database successfully seeded with demonstration data!"))

