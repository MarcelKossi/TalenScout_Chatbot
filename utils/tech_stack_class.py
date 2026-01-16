class TechStackClassifier:
    """
    A deterministic, rule-based classifier that:
    - normalizes raw tech stack input
    - removes duplicates
    - categorizes technologies into buckets
    - handles unknown items gracefully
    """

    def __init__(self, tech_list):
        """
        tech_list is expected to be a list of raw tech strings
        already validated by Validators.validate_tech_stack().
        """
        self.raw_list = tech_list
        self.cleaned_list = self._normalize(tech_list)
        self.categorized = self._categorize(self.cleaned_list)

    # NORMALIZATION
    def _normalize(self, tech_list):
        """
        Clean each technology string:
        - strip whitespace
        - preserve original casing for readability
        - remove duplicates while keeping order
        """

        seen = set()
        cleaned = []

        for item in tech_list:
            text = item.strip()
            if text and text not in seen:
                seen.add(text)
                cleaned.append(text)

        return cleaned

    # CATEGORIES
    def _categorize(self, items):
        """
        Categorize technologies into buckets.
        Unknown techs go into the 'other' category.
        """

        languages = {
            "Python", "Java", "C#", "C++", "JavaScript", "TypeScript", "Go", "Rust",
            "Ruby", "PHP", "Kotlin", "Swift"
        }

        frameworks = {
            "Django", "Flask", "React", "Angular", "Vue", "Spring", "Laravel",
            "Node.js", "Express", "FastAPI", "React Native"
        }

        databases = {
            "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "SQL Server",
            "Redis", "MariaDB", "Cassandra"
        }

        tools = {
            "Git", "Docker", "Kubernetes", "Jenkins", "CI/CD", "GitHub Actions",
            "Terraform", "Ansible"
        }

        cloud = {
            "AWS", "Azure", "Google Cloud", "Azure DevOps"
        }

        categorized = {
            "languages": [],
            "frameworks": [],
            "databases": [],
            "tools": [],
            "cloud": [],
            "other": []
        }

        for tech in items:
            if tech in languages:
                categorized["languages"].append(tech)
            elif tech in frameworks:
                categorized["frameworks"].append(tech)
            elif tech in databases:
                categorized["databases"].append(tech)
            elif tech in tools:
                categorized["tools"].append(tech)
            elif tech in cloud:
                categorized["cloud"].append(tech)
            else:
                categorized["other"].append(tech)

        return categorized
    
    # PUBLIC METHODS
    def get_clean_list(self):
        """Return normalized list, no duplicates."""
        return self.cleaned_list

    def get_categories(self):
        """Return tech stack categorized into buckets."""
        return self.categorized

    def get_for_question_generation(self):
        """
        Return a flat list of technologies to generate questions for.
        Combines all categories into a single list.
        """
        output = []
        for category in self.categorized.values():
            output.extend(category)
        return output
