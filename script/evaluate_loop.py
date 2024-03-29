import numpy as np
import torch
from torch.nn import Module
from torch.utils.data import DataLoader

from tools import ClassificationMetrics


def evaluate_loop(network: Module, dataloader: DataLoader, criterion: Module, **kwargs):
    device = kwargs["device"]
    print_step_test = kwargs.get("print_step_test")
    num_batches = len(dataloader)
    digits = int(np.log10(num_batches)) + 1  # for print

    total_loss = 0  # BCE loss
    all_labels = []
    all_outputs = []
    with torch.no_grad():
        for batch_idx, (images, labels) in enumerate(dataloader):
            images, labels = images.to(device), labels.to(device)

            network.eval()
            outputs = network(images)
            loss = criterion(outputs, labels)

            total_loss += loss.item()
            all_labels += labels.tolist()
            all_outputs += outputs.tolist()

            if print_step_test is not None and batch_idx % print_step_test == 0:
                metrics = ClassificationMetrics(labels, outputs)
                print(f"[Batch {batch_idx:{digits}d}/{num_batches}] "
                      f"Loss: {loss.item():.4f}, "
                      f"Accuracy: {metrics.accuracy:.2%}")

    total_loss /= len(dataloader)
    print(f"Total test data: {len(all_labels)}, Loss: {total_loss:.4f}")
    metrics = ClassificationMetrics(all_labels, all_outputs)
    metrics.print_report()
