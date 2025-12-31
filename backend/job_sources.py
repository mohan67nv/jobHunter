"""
German Job Board Configuration
Complete list of job sources for the German market
"""

# Core Job Boards ("Big 5")
CORE_BOARDS = {
    'arbeitsagentur': {
        'name': 'Arbeitsagentur',
        'url': 'https://www.arbeitsagentur.de',
        'type': 'official',
        'active': True,
        'priority': 1,
        'description': 'German Federal Employment Agency'
    },
    'stepstone': {
        'name': 'StepStone',
        'url': 'https://www.stepstone.de',
        'type': 'job_board',
        'active': True,
        'priority': 1,
        'description': 'Premium professional roles'
    },
    'indeed': {
        'name': 'Indeed Germany',
        'url': 'https://de.indeed.com',
        'type': 'aggregator',
        'active': True,
        'priority': 1,
        'description': 'Largest job aggregator'
    },
    'linkedin': {
        'name': 'LinkedIn',
        'url': 'https://www.linkedin.com',
        'type': 'network',
        'active': True,
        'priority': 1,
        'description': 'International professional network'
    },
    'xing': {
        'name': 'XING Jobs',
        'url': 'https://www.xing.com/jobs',
        'type': 'network',
        'active': True,
        'priority': 1,
        'description': 'DACH region professional network'
    },
}

# Tech, Engineering & STEM
TECH_BOARDS = {
    'germantechjobs': {
        'name': 'GermanTechJobs',
        'url': 'https://germantechjobs.de',
        'type': 'tech',
        'active': True,
        'priority': 2,
        'description': 'Tech with salary transparency'
    },
    'honeypot': {
        'name': 'Honeypot',
        'url': 'https://www.honeypot.io',
        'type': 'tech',
        'active': True,
        'priority': 2,
        'description': 'Developer matching platform'
    },
    'jobvector': {
        'name': 'Jobvector',
        'url': 'https://www.jobvector.de',
        'type': 'tech',
        'active': True,
        'priority': 2,
        'description': 'Science, Tech, Engineering, Medical'
    },
    'stackoverflow': {
        'name': 'Stack Overflow Jobs',
        'url': 'https://stackoverflow.com/jobs',
        'type': 'tech',
        'active': True,
        'priority': 2,
        'description': 'Global tech standard'
    },
    'gulp': {
        'name': 'Gulp',
        'url': 'https://www.gulp.de',
        'type': 'tech',
        'active': True,
        'priority': 2,
        'description': 'IT and Engineering freelancers'
    },
    '4scotty': {
        'name': '4Scotty',
        'url': 'https://www.4scotty.com',
        'type': 'tech',
        'active': True,
        'priority': 2,
        'description': 'Tech-focused reverse hiring'
    },
    'itjobs': {
        'name': 'IT-Jobs.de',
        'url': 'https://www.it-jobs.de',
        'type': 'tech',
        'active': True,
        'priority': 2,
        'description': 'General IT roles'
    },
}

# Startups & English-Speaking
STARTUP_BOARDS = {
    'berlinstartupjobs': {
        'name': 'Berlin Startup Jobs',
        'url': 'https://berlinstartupjobs.com',
        'type': 'startup',
        'active': True,
        'priority': 2,
        'description': 'Berlin startup ecosystem'
    },
    'arbeitnow': {
        'name': 'Arbeitnow',
        'url': 'https://www.arbeitnow.com',
        'type': 'startup',
        'active': True,
        'priority': 2,
        'description': 'English-speaking with visa support'
    },
    'englishjobs': {
        'name': 'EnglishJobs.de',
        'url': 'https://www.englishjobs.de',
        'type': 'startup',
        'active': True,
        'priority': 2,
        'description': 'International candidate focus'
    },
    'gruenderszene': {
        'name': 'Gründerszene',
        'url': 'https://jobs.gruenderszene.de',
        'type': 'startup',
        'active': True,
        'priority': 2,
        'description': 'Startup economy'
    },
    'thelocal': {
        'name': 'The Local Jobs',
        'url': 'https://www.thelocal.de/jobs',
        'type': 'startup',
        'active': True,
        'priority': 2,
        'description': 'Expats and English-speaking'
    },
}

# Aggregators & Meta-Search
AGGREGATOR_BOARDS = {
    'kimeta': {
        'name': 'Kimeta',
        'url': 'https://www.kimeta.de',
        'type': 'aggregator',
        'active': True,
        'priority': 1,
        'description': 'Comprehensive meta-search'
    },
    'joblift': {
        'name': 'Joblift',
        'url': 'https://www.joblift.de',
        'type': 'aggregator',
        'active': True,
        'priority': 1,
        'description': 'Meta-search engine'
    },
    'jooble': {
        'name': 'Jooble',
        'url': 'https://de.jooble.org',
        'type': 'aggregator',
        'active': True,
        'priority': 1,
        'description': 'Aggregator of smaller boards'
    },
    'adzuna': {
        'name': 'Adzuna',
        'url': 'https://www.adzuna.de',
        'type': 'aggregator',
        'active': True,
        'priority': 1,
        'description': 'Value-based search'
    },
    'monster': {
        'name': 'Monster.de',
        'url': 'https://www.monster.de',
        'type': 'aggregator',
        'active': True,
        'priority': 1,
        'description': 'Traditional generalist'
    },
}

# Creative, Media & Business
CREATIVE_BOARDS = {
    'dasauge': {
        'name': 'Dasauge',
        'url': 'https://www.dasauge.de',
        'type': 'creative',
        'active': True,
        'priority': 3,
        'description': 'Design, Photo, Creative'
    },
    'efinancialcareers': {
        'name': 'eFinancialCareers',
        'url': 'https://www.efinancialcareers.de',
        'type': 'business',
        'active': True,
        'priority': 3,
        'description': 'Banking & Finance'
    },
    'experteer': {
        'name': 'Experteer',
        'url': 'https://www.experteer.de',
        'type': 'executive',
        'active': True,
        'priority': 3,
        'description': 'Senior Management (€60k+)'
    },
}

# Combine all sources
ALL_JOB_SOURCES = {
    **CORE_BOARDS,
    **TECH_BOARDS,
    **STARTUP_BOARDS,
    **AGGREGATOR_BOARDS,
    **CREATIVE_BOARDS,
}

# Priority-based source selection
def get_sources_by_priority(priority: int = None):
    """Get job sources filtered by priority level"""
    if priority is None:
        return list(ALL_JOB_SOURCES.keys())
    return [k for k, v in ALL_JOB_SOURCES.items() if v['priority'] == priority]

def get_active_sources():
    """Get only active job sources"""
    return [k for k, v in ALL_JOB_SOURCES.items() if v['active']]

def get_sources_by_type(source_type: str):
    """Get sources by type (tech, startup, aggregator, etc.)"""
    return [k for k, v in ALL_JOB_SOURCES.items() if v['type'] == source_type]

# Recommended source combinations for different use cases
RECOMMENDED_COMBINATIONS = {
    'tech_developer': ['germantechjobs', 'stackoverflow', 'honeypot', 'linkedin', 'stepstone'],
    'startup_english': ['berlinstartupjobs', 'arbeitnow', 'englishjobs', 'thelocal', 'linkedin'],
    'comprehensive': ['arbeitsagentur', 'kimeta', 'joblift', 'indeed', 'linkedin', 'stepstone'],
    'quick_scan': ['kimeta', 'joblift', 'indeed'],  # Aggregators give broad coverage fast
    'premium': ['stepstone', 'experteer', 'linkedin', 'xing'],
}
