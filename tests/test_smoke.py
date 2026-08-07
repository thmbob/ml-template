"""Test smoke pour valider l'environnement de base et le package."""

import torch


def test_import_package() -> None:
    """Vérifie que le package principal s'importe sans erreur."""
    import mon_projet_ml

    assert mon_projet_ml is not None


def test_pytorch_functionality() -> None:
    """Vérifie que les tenseurs PyTorch réagissent correctement."""
    x = torch.tensor([1.0, 2.0, 3.0])
    y = x + 2.0
    assert torch.allclose(y, torch.tensor([3.0, 4.0, 5.0]))
