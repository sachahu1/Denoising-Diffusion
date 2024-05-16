import abc

import torch


class BaseBetaScheduler:
  def __init__(self, steps: int):
    self.steps = steps
    self.betas = self.sample_betas()
    self.alpha_bars = self.compute_alpha_bar()

  @abc.abstractmethod
  def sample_betas(self):
    pass

  @abc.abstractmethod
  def compute_alpha_bar(self):
    pass

  def to(self, device: str):
    self.betas = self.betas.to(device)
    self.alpha_bars = self.alpha_bars.to(device)
    return self

class LinearBetaScheduler(BaseBetaScheduler):
  def __init__(
    self,
    beta_start: float = 0.0001,
    beta_end: float = 0.02,
    steps: int = 1000,
  ):
    self.beta_start = beta_start
    self.beta_end = beta_end
    super().__init__(steps)

  def sample_betas(self):
    return torch.linspace(self.beta_start, self.beta_end, self.steps)

  def compute_alpha_bar(self):
    alphas = 1 - self.betas
    alpha_bar = torch.cumprod(alphas, dim=0)
    return alpha_bar