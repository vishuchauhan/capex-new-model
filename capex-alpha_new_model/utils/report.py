def generate_strategy_report(sharpe, total_return):

    print("\n===== STRATEGY REPORT =====")

    print(f"Total Return: {round(total_return,2)}")
    print(f"Sharpe Ratio: {round(sharpe,2)}")

    print("\nStrategy Explanation:")
    print("This is a multi-agent investment model.")
    print("Financial Agent → evaluates growth signals")
    print("Industry Agent → detects sector expansion")
    print("Strategy Agent → applies game theory")

    print("\nHow to Use:")
    print("1. Run model monthly")
    print("2. Select top stocks")
    print("3. Invest equally")
    print("4. Rebalance every month")

    print("\n===========================")