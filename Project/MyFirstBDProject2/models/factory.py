"""
Factory for the different types of repositories.
"""

def create_repository():
    """Creates a repository from its name and settings. The settings
    is a dictionary where the keys are different for every type of repository.
    See each repository for details on the required settings."""

    from.panda import Repository
    return Repository()
