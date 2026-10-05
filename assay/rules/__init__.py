"""Rules as pure functions over typed models.

Each returns a list of problems (empty = passes). The same functions run
twice: as agent validators (problems go back to the model to fix) and as
stage gates (problems stop the graph). One definition of every rule.
"""
