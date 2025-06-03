import math

class Pricer:
  def __init__(self, option):
    if option not in ["call", "put"]:
      raise ValueError("Invalid option type: " + option)
    else:
      self.option = option

  # Create stock tree and return step, growth, u, d, p, q
  def binomial(self, S, r, t, n, sigma):
    step = t / n
    growth = math.exp(r * step)
    u = math.exp(sigma * step**(1/2))
    d = 1 / u
    p = (growth - d) / (u - d)
    q = 1 - p
    tree = [[S * u**j * d**(i - j) for j in range(i + 1)] for i in range(n + 1)]
    return [step, growth, u, d, p, q, tree]

  # Create option tree and return price of option
  def price(self, S, K, r, t, n, sigma):
    step, growth, u, d, p, q, tree = self.binomial(S, r, t, n, sigma)
    for j in range(n + 1):
      tree[n][j] = max(0, tree[n][j] - K) if self.option == "call" else max(0, K - tree[n][j])
    for i in range(n - 1, -1, -1):
      for j in range(i, -1, -1):
        tree[i][j] = (p * tree[i + 1][j + 1] + q * tree[i + 1][j]) / growth
    return [tree[0][0], tree]

  def theta(self, tree, t, n):
    return (tree[0][0] - tree[2][1]) / (t * 365 / n)

  def delta(self, optionTree, stockTree):
    return (optionTree[1][1] - optionTree[1][0]) / (stockTree[1][1] - stockTree[1][0])
    

call = Pricer("call")
_, _, _, _, _, _, stockTree = call.binomial(S = 203.22, r = 4.41 / 100, t = 3 / 365, n = 1000, sigma = 28.22 / 100)
price28, optionTree = call.price(S = 203.22, K = 207.5, r = 4.41 / 100, t = 3 / 365, n = 1000, sigma = 28 / 100)
price50, optionTree = call.price(S = 203.22, K = 207.5, r = 4.41 / 100, t = 3 / 365, n = 1000, sigma = 50 / 100)
d = call.delta(optionTree, stockTree)
print(f'price28: {price28}')
print(f'price50: {price50}')