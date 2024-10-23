from slickrpc import Proxy
import json

class NodeRpc:
    def __init__(self, rpc_user, rpc_password, rpc_port, node_ip):
        self.rpc_connection = self.rpc_connect(rpc_user, rpc_password, rpc_port, node_ip)


    def rpc_connect(self, rpc_user, rpc_password, rpc_port, node_ip):
        try:
            rpc_connection = Proxy(f"http://{rpc_user}:{rpc_password}@{node_ip}:{rpc_port}")
        except Exception as e:
            raise Exception(f"Connection error: {e}")
        return rpc_connection


    def import_priv_key(self, priv_key):
        try:
            self.rpc_connection.importprivkey(priv_key)
        except Exception as e:
            raise Exception(f"Error importing private key: {e}")


    def get_balance(self, addr):
        try:
            balance = self.rpc_connection.getbalance()
        except Exception as e:
            raise Exception(f"Error getting balance: {e}")
        return balance


    def get_utxos(self, addr):
        try:
            utxos = self.rpc_connection.listunspent(1, 9999999, [addr])
        except Exception as e:
            raise Exception(f"Error getting UTXOs: {e}")
        return utxos


    def get_transaction(self, txid):
        try:
            transaction = self.rpc_connection.gettransaction(txid)
        except Exception as e:
            raise Exception(f"Error getting transaction: {e}")
        return transaction


    def get_network_status(self):
        try:
            info = self.rpc_connection.getinfo()
        except Exception as e:
            raise Exception(f"Error getting network status: {e}")
        return info


    def broadcast(self, signedtx):
        # print(f"Broadcasting {signedtx}")
        try:
            tx_id = self.rpc_connection.sendrawtransaction(signedtx)
        except Exception as e:
            raise Exception(f"Error broadcasting transaction: {e}")
        return tx_id


    def get_info(self):
        try:
            info = self.rpc_connection.getinfo()
        except Exception as e:
            raise Exception(f"Error getting node info: {e}")
        return info


    def get_currency_state(self, currency_name, height_range=''):
        try:
            currency_state_result = self.rpc_connection.getcurrencystate(currency_name, height_range)
        except Exception as e:
            raise Exception(f"Error retrieving currency state: {e}")
        return currency_state_result

    def get_pending_transfers(self, currency_name):
        try:
            pending_transfers_result = self.rpc_connection.getpendingtransfers(currency_name)
        except Exception as e:
            raise Exception(f"Error retrieving pending transfers in {currency_name}: {e}")
        return pending_transfers_result
    
    
    def get_imports(self, currency_name, start_height, end_height=''):
        try:
            get_imports_result = self.rpc_connection.getimports(currency_name, start_height)
        except Exception as e:
            raise Exception(f"Error retrieving get imports in {currency_name} start height {start_height}: {e}")
        return get_imports_result


    def send_currency(self, from_address, params):
        # print(from_address)
        # print(params)
        try:
            send_currency_result = self.rpc_connection.sendcurrency(from_address, params)
        except Exception as e:
            raise Exception(f"Error sending currency: {e}")
        return send_currency_result


    def send_currency_simple_to_identity(self, from_address, currency, identity, amount):
        # params = [{"currency": currency, "address": identity, "amount": amount}]
        # print(params)
        return self.send_currency(from_address, params)


    def send_currency_via(self, currency, convertto, via, amount, address):
        # params = [{"currency": currency, "convertto": convertto, "via": via, "amount": amount, "address": address}]
        # print(f"send currency params: {params}")
        try:
            send_currency_result = self.send_currency(address, params)
        except Exception as e:
            raise Exception(f"Error sending currency: {e}")
        return send_currency_result


    def get_wallet_info(self):
        try:
            result = self.rpc_connection.getwalletinfo()
        except Exception as e:
            raise Exception(f"Error retrieving wallet info: {e}")
        return result


    def z_get_operation_status(self, opid):
        opids = [opid]
        # print(f"z {opids}")
        try:
            result = self.rpc_connection.z_getoperationstatus(opids)
            # print(result)
        except Exception as e:
            raise Exception(f"Error retrieving operation status: {e}")
        return result


    def register_name_commitment(self, name, primary_raddress, referral_id, parent="VRSC", source_of_funds="*"):
        try:
            result = self.rpc_connection.registernamecommitment(name, primary_raddress, referral_id, parent, source_of_funds)
        except Exception as e:
            raise Exception(f"Error with registering name commitment: {e}")
        return result


    def register_identity(self, json_namecommitment_response, json_identity, source_of_funds, fee_offer=80):
        # json_identity is an object added to the namecommitment result object as identity attribute
        json_namecommitment_response["identity"] = json_identity
        print(json_namecommitment_response)
        try:
            result = self.rpc_connection.registeridentity(json_namecommitment_response, False, fee_offer, source_of_funds)
        except Exception as e:
            raise Exception(f"Error with registering identity: {e}")
        return result


    def update_identity(self):
        pass
#"params": [
# {
#   "name":"dude",
#   "contentmultimap":
#     { "iCtawpxUiCc2sEupt7Z4u8SDAncGZpgSKm": [
#        {"i4GC1YGEVD21afWudGoFJVdnfjJ5XWnCQv":{
#           "version":1,
#           "flags":0,
#           "label":"dude.vrsc::nft.simple.name",
#           "mimetype":"text/plain",
#           "objectdata":{
#              "message":"dudes nft"
#            }
#         }
#      },
#      {
#         "data": {
#            "createmmr":true,
#            "mmrdata":[
#              {"filename":"/Users/dude/Desktop/dude.png","mimetype":"picture/PNG"}
#            ]
#          }
#       }
#     ]
#    }
#   }
#  ]}

    def get_raw_transaction(self, txid, verbose=1):
        try:
            result = self.rpc_connection.getrawtransaction(txid, verbose)
        except Exception as e:
            raise Exception(f"Error with get raw transaction: {e}")
        return result


    def define_currency(self, params):
        try:
            result = self.rpc_connection.definecurrency(params)
        except Exception as e:
            raise Exception(f"Error with define currency: {e}")
        print(json.dumps(result))
        return self.broadcast(result["hex"])


    def define_simple_token_currency(self, options, name, id_registration_fees, pre_allocations, proof_protocol):
        params = {"options": options, "name": name, "idregistrationfees": id_registration_fees, "preallocations": pre_allocations, "proofprotocol": proof_protocol}
        try:
            result = self.rpc_connection.definecurrency(params)
        except Exception as e:
            raise Exception(f"Error with define simple token currency: {e}")
        print(json.dumps(result))
        return self.broadcast(result["hex"])

    def define_define_id_control_token(self, options, name, pre_allocations):
        params = {"options": options, "name": name, "preallocations": pre_allocations, "maxpreconversion": [0]}
        # print(params)
        try:
            result = self.rpc_connection.definecurrency(params)
        except Exception as e:
            raise Exception(f"Error with define id control token currency: {e}")
        print(json.dumps(result))
        return self.broadcast(result["hex"])



    def get_currency_balance(self, from_address):
        try:
            result = self.rpc_connection.getcurrencybalance(from_address)
        except Exception as e:
            raise Exception(f"Error with get currency balance: {e}")
        return result


    def get_currency(self, currency_name_or_id):
        try:
            result = self.rpc_connection.getcurrency(currency_name_or_id)
        except Exception as e:
            raise Exception(f"Error with get currency: {e}")
        return result


    def get_identity(self, identity_name_or_id):
        try:
            result = self.rpc_connection.getidentity(identity_name_or_id)
        except Exception as e:
            raise Exception(f"Error with get identity: {e}")
        return result


    def estimate_conversion(self, currency_sent, via, currency_received, amount):
        params = {"currency": currency_sent, "convertto": currency_received, "via": via, "amount": amount}
        if via == currency_received or via == currency_sent:
            del params["via"]

        # print(params)
        try:
            result = self.rpc_connection.estimateconversion(params)
        except Exception as e:
            raise Exception(f"Error with estimate conversion: {e}")
        return result

    def get_address_balance(self, raddress):
        params = {"addresses": [raddress], "friendlynames": 1}
        try:
            result = self.rpc_connection.getaddressbalance(params)
        except Exception as e:
            raise Exception(f"Error with estimate conversion: {e}")
        return result
