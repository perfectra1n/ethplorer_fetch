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
    try:
        try:
            response.json()["tokens"]
        except KeyError:
            print(f"No tokens were found for address: '{address}'.")
            return
        address_tokens = {response.json()["address"]: response.json()["tokens"]}
    except KeyError as e:
        print("Something had an absolute STROKE!")
        print(e)
        print("Response from server:")
        print(response.text)

    return address_tokens


def get_number_and_value_of_tokens(address_tokens):
    for address, tokens in address_tokens.items():
        for token in tokens:
            num_of_tokens = float(token["rawBalance"]) / 10 ** int(
                token["tokenInfo"]["decimals"]
            )

            # Check if the token even has a price, if it's false, that means that it's most likely a scam coin.
            if token["tokenInfo"]["price"]:
                token_value_in_usd = num_of_tokens * token["tokenInfo"]["price"]["rate"]

                # Make sure that this token's value is > 1 dollar
                if token_value_in_usd > 1:

                    # Check to see if we're already storing this coin
                    token_found = False
                    for token_dict in list_of_token_dicts:
                        if token["tokenInfo"]["name"] == token_dict["name"]:
                            token_dict["value"] += token_value_in_usd
                            token_found = True
                            break
                    if not token_found:
                        list_of_token_dicts.append(
                            {
                                "name": token["tokenInfo"]["name"],
                                "value": token_value_in_usd,
                            }
                        )
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

    list_of_token_dicts = []

    print("Starting to fetch now...")

    for address in args.addresses:
        tokens = fetch_address_tokens(address)
        if tokens:
            get_number_and_value_of_tokens(tokens)

    # Sort the list according to the value in each dictionary
    # https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
    new_list = sorted(list_of_token_dicts, key=lambda k: k["value"])
    new_list.reverse()

    print()
    print("Pretty printing data...")
    for coin in new_list:
        print()
        print("----------- New Coin -----------")
        print(coin["name"])
        print(f"{coin['value']} USD")
        print("--------------------------------")
        print()
