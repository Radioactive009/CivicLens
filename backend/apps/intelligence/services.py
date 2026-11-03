import re

POSITIVE_KEYWORDS = {'boost', 'improved', 'growth', 'inaugurated', 'success', 'expand', 'awarded', 'welfare', 'developed', 'completed', 'progress', 'sanctioned', 'approval', 'record'}
CONCERN_KEYWORDS = {'protest', 'delay', 'crisis', 'shortage', 'complaint', 'strike', 'pollution', 'accident', 'unemployment', 'deficit', 'waterlogging', 'criticism', 'damage', 'struggle', 'neglect', 'demands'}

TOPIC_MAPPINGS = {
    'EDUCATION': ['school', 'college', 'university', 'student', 'teacher', 'syllabus', 'exam', 'literacy', 'education', 'iit', 'iim', 'scholarship'],
    'HEALTHCARE': ['hospital', 'doctor', 'clinic', 'medical', 'health', 'disease', 'patient', 'ayushman', 'phc', 'ambulance', 'medicine'],
    'EMPLOYMENT': ['job', 'unemployment', 'hiring', 'recruitment', 'worker', 'industry', 'wage', 'salary', 'factory', 'manpower', 'skills'],
    'AGRICULTURE': ['crop', 'farmer', 'mandi', 'paddy', 'wheat', 'kharif', 'rabi', 'fertilizer', 'kisan', 'irrigation', 'procurement', 'msp'],
    'INFRASTRUCTURE': ['highway', 'road', 'expressway', 'bridge', 'flyover', 'sewerage', 'drainage', 'power', 'electricity', 'water supply', 'construction'],
    'ENVIRONMENT': ['pollution', 'air quality', 'aqi', 'stubble', 'water table', 'groundwater', 'waste', 'forest', 'yamuna', 'climate'],
    'TRANSPORTATION': ['bus', 'train', 'metro', 'railway', 'traffic', 'transport', 'roadways', 'depot', 'fare'],
    'PUBLIC_SERVICES': ['panchayat', 'municipal', 'ration', 'portal', 'pension', 'citizen', 'governance', 'subdivision', 'collector', 'tehsil']
}

HARYANA_DISTRICTS = [
    'Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Gurugram',
    'Hisar', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh',
    'Nuh', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat', 'Yamunanagar'
]

def analyze_article_text(title, description, content=''):
    full_text = f"{title} {description} {content}".lower()
    words = set(re.findall(r'\b[a-z]{3,}\b', full_text))

    # Topic classification
    best_category = 'PUBLIC_SERVICES'
    max_topic_score = 0
    matched_keywords = []

    for cat, keywords in TOPIC_MAPPINGS.items():
        matches = [kw for kw in keywords if kw in full_text]
        if len(matches) > max_topic_score:
            max_topic_score = len(matches)
            best_category = cat
        matched_keywords.extend(matches)

    # Geographic reference detection
    detected_geo = 'Haryana'
    for dist in HARYANA_DISTRICTS:
        if dist.lower() in full_text:
            detected_geo = dist
            break

    # Sentiment classification
    pos_count = sum(1 for w in POSITIVE_KEYWORDS if w in full_text)
    neg_count = sum(1 for w in CONCERN_KEYWORDS if w in full_text)

    if pos_count > neg_count:
        score = min(1.0, 0.25 + (pos_count - neg_count) * 0.2)
        label = 'POSITIVE'
    elif neg_count > pos_count:
        score = max(-1.0, -0.25 - (neg_count - pos_count) * 0.2)
        label = 'CONCERN'
    else:
        score = 0.0
        label = 'NEUTRAL'

    return {
        'category': best_category,
        'sentiment_label': label,
        'sentiment_score': round(score, 2),
        'geographic_reference': detected_geo,
        'keywords': list(set(matched_keywords))[:8]
    }

