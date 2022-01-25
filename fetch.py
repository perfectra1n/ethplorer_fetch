import requests
import argparse


def make_request(
    method="GET",
    host="https://api.ethplorer.io",
    path="/getLastBlock",
    params={},
):
    if "apiKey" not in params:
        params["apiKey"] = args.ethplorer_apikey
    response = requests.request(method, f"{host}{path}", params=params)

    if response.status_code != 200:
        print("Ethplorer response was not okay.")
    return response


def fetch_address_tokens(address: str):
    params = {"showEthtotals": "true"}
    response = make_request(path=f"/getAddressInfo/{address}", params=params)
    address_tokens = {response.json()["address"]: response.json()["tokens"]}

    return address_tokens

def get_number_of_tokens(address_tokens):
    for address, tokens in address_tokens.items():
        for token in tokens:
            num_of_tokens = float(token["rawBalance"]) / 10**int(token["tokenInfo"]["decimals"])

            if token["tokenInfo"]["price"]:
                token_value_in_usd = num_of_tokens * token["tokenInfo"]["price"]["rate"]
                if token_value_in_usd > 1:
                    print(token["tokenInfo"]["name"])
                    print(token_value_in_usd)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This is the description for the main parser!"
    )
    parser.add_argument(
        "ethplorer_apikey",
        help="Required. Provide your API key for Ethplorer.",
    )
    parser.add_argument(
        "-a",
        "--addresses",
        nargs="+",
        help="The addresses that you would like to fetch in quotes, separated by a space. e.g. '0x123123 0x123124'",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Optional. Use this argument if you are debugging any errors.",
    )

    args = parser.parse_args()

    print("Starting to fetch now...")

    get_number_of_tokens(fetch_address_tokens("0x7496B3EB2a23d5ee2F23a9B29c93e14F1873DF52"))