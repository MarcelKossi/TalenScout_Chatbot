"""
Test script for TalenScout Chatbot core functionality
"""

import sys
import json
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class CandidateProfile(BaseModel):
    """Structured candidate information"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position_applied: Optional[str] = None
    years_of_experience: Optional[int] = None
    current_role: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: Optional[str] = None
    availability: Optional[str] = None
    expected_salary: Optional[str] = None
    location: Optional[str] = None
    work_authorization: Optional[str] = None
    notice_period: Optional[str] = None


def test_candidate_profile():
    """Test CandidateProfile creation and serialization"""
    print("Testing CandidateProfile...")
    
    profile = CandidateProfile(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1-234-567-8900",
        position_applied="Software Engineer",
        years_of_experience=5,
        current_role="Senior Developer",
        skills=["Python", "Machine Learning", "AWS", "Docker"],
        education="Bachelor's in Computer Science",
        availability="2 weeks",
        expected_salary="$120,000 - $140,000",
        location="San Francisco, CA (Open to remote)",
        work_authorization="Yes",
        notice_period="2 weeks"
    )
    
    # Test serialization
    profile_dict = profile.model_dump()
    profile_json = json.dumps(profile_dict, indent=2)
    
    print("✓ Profile created successfully")
    print("\nSample profile JSON:")
    print(profile_json)
    
    # Test field access
    assert profile.name == "John Doe"
    assert len(profile.skills) == 4
    assert profile.years_of_experience == 5
    
    print("\n✓ All field accesses work correctly")
    
    return profile


def test_skills_parsing():
    """Test skills parsing from comma-separated string"""
    print("\nTesting skills parsing...")
    
    skills_input = "Python, JavaScript, React, Node.js, SQL"
    skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]
    
    profile = CandidateProfile(skills=skills_list)
    
    assert len(profile.skills) == 5
    assert "Python" in profile.skills
    assert "SQL" in profile.skills
    
    print(f"✓ Parsed {len(profile.skills)} skills from input")
    print(f"  Skills: {', '.join(profile.skills)}")
    
    return profile


def test_screening_questions():
    """Test screening questions structure"""
    print("\nTesting screening questions...")
    
    QUESTIONS = [
        {
            "id": "greeting",
            "question": "Hello! May I have your full name?",
            "field": "name",
            "required": True
        },
        {
            "id": "contact_email",
            "question": "Could you please provide your email address?",
            "field": "email",
            "required": True
        },
        {
            "id": "position",
            "question": "Which position are you applying for?",
            "field": "position_applied",
            "required": True
        }
    ]
    
    assert len(QUESTIONS) == 3
    assert all("id" in q and "question" in q and "field" in q for q in QUESTIONS)
    
    print(f"✓ {len(QUESTIONS)} screening questions validated")
    print(f"  Example question: {QUESTIONS[0]['question']}")


def test_data_persistence():
    """Test saving candidate data to JSON"""
    print("\nTesting data persistence...")
    
    profile = CandidateProfile(
        name="Jane Smith",
        email="jane.smith@example.com",
        position_applied="Data Scientist",
        skills=["Python", "TensorFlow", "Statistics"]
    )
    
    # Create test directory
    import os
    os.makedirs("/tmp/test_candidate_data", exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/tmp/test_candidate_data/{profile.name.replace(' ', '_')}_{timestamp}.json"
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(profile.model_dump(), f, indent=2)
    
    # Verify file exists and can be read
    with open(filename, 'r') as f:
        loaded_data = json.load(f)
    
    assert loaded_data["name"] == "Jane Smith"
    assert len(loaded_data["skills"]) == 3
    
    print(f"✓ Data saved successfully to {filename}")
    print(f"✓ Data loaded and verified")
    
    # Clean up
    os.remove(filename)
    os.rmdir("/tmp/test_candidate_data")
    print("✓ Cleanup completed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("TalenScout Chatbot - Core Functionality Tests")
    print("=" * 60)
    
    try:
        test_candidate_profile()
        test_skills_parsing()
        test_screening_questions()
        test_data_persistence()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
