def main() -> None:
    from pathlib import Path

    import torch
    import torch.nn as nn
    import torch.optim as optim
    from sklearn.datasets import make_moons
    from sklearn.model_selection import train_test_split
    from torch.utils.data import DataLoader, TensorDataset

    # Chemins relatifs basés sur la structure du projet
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    EXP_DIR = BASE_DIR / "experiments"

    DATA_DIR.mkdir(exist_ok=True)
    EXP_DIR.mkdir(exist_ok=True)

    # 1. Dataset jouet (Simule le téléchargement / préparation)
    print("-> Préparation du dataset dans data/...")
    X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    train_dataset = TensorDataset(torch.FloatTensor(X_train), torch.LongTensor(y_train))
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # 2. Détection du hardware (CPU / GPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"-> Matériel utilisé : {device}")
    if device.type == "cuda":
        print(f"   GPU détecté : {torch.cuda.get_device_name(0)}")

    # 3. Modèle jouet (MLP simple)
    class ToyMLP(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.net = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.net(x)

    model = ToyMLP().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    # 4. Boucle d'entraînement
    print("-> Lancement de l'entraînement...")
    epochs = 50
    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            optimizer.zero_grad()
            output = model(batch_x)
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"   Epoch {epoch + 1}/{epochs} - Loss: {total_loss / len(train_loader):.4f}")

    # 5. Sauvegarde des résultats dans experiments/
    model_path = EXP_DIR / "toy_model.pt"
    torch.save(model.state_dict(), model_path)
    print(f"-> Modèle et résultats sauvegardés avec succès dans {EXP_DIR}/")


if __name__ == "__main__":
    main()
