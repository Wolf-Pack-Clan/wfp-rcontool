import socket
import json
from re import split as splitstr
from re import sub

from kivy.utils import hex_colormap

#global valid_colors
valid_colors = ['Aliceblue', 'Antiquewhite', 'Aqua', 'Aquamarine', 'Azure',
                'Beige', 'Bisque', 'Black', 'Blanchedalmond', 'Blue', 'Blueviolet',
                'Brown', 'Burlywood', 'Cadetblue', 'Chartreuse', 'Chocolate', 'Coral',
                'Cornflowerblue', 'Cornsilk', 'Crimson', 'Cyan', 'Darkblue', 'Darkcyan',
                'Darkgoldenrod', 'Darkgray', 'Darkgrey', 'Darkgreen', 'Darkkhaki', 'Darkmagenta',
                'Darkolivegreen', 'Darkorange', 'Darkorchid', 'Darkred', 'Darksalmon', 'Darkseagreen',
                'Darkslateblue', 'Darkslategray', 'Darkslategrey', 'Darkturquoise', 'Darkviolet',
                'Deeppink', 'Deepskyblue', 'Dimgray', 'Dimgrey', 'Dodgerblue', 'Firebrick',
                'Floralwhite', 'Forestgreen', 'Fuchsia', 'Gainsboro', 'Ghostwhite', 'Gold',
                'Goldenrod', 'Gray', 'Grey', 'Green', 'Greenyellow', 'Honeydew', 'Hotpink',
                'Indianred', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'Lavenderblush', 'Lawngreen',
                'Lemonchiffon', 'Lightblue', 'Lightcoral', 'Lightcyan', 'Lightgoldenrodyellow',
                'Lightgreen', 'Lightgray', 'Lightgrey', 'Lightpink', 'Lightsalmon', 'Lightseagreen',
                'Lightskyblue', 'Lightslategray', 'Lightslategrey', 'Lightsteelblue', 'Lightyellow',
                'Lime', 'Limegreen', 'Linen', 'Magenta', 'Maroon', 'Mediumaquamarine', 'Mediumblue',
                'Mediumorchid', 'Mediumpurple', 'Mediumseagreen', 'Mediumslateblue', 'Mediumspringgreen',
                'Mediumturquoise', 'Mediumvioletred', 'Midnightblue', 'Mintcream', 'Mistyrose',
                'Moccasin', 'Navajowhite', 'Navy', 'Oldlace', 'Olive', 'Olivedrab', 'Orange',
                'Orangered', 'Orchid', 'Palegoldenrod', 'Palegreen', 'Paleturquoise', 'Palevioletred',
                'Papayawhip', 'Peachpuff', 'Peru', 'Pink', 'Plum', 'Powderblue', 'Purple', 'Red',
                'Rosybrown', 'Royalblue', 'Saddlebrown', 'Salmon', 'Sandybrown', 'Seagreen',
                'Seashell', 'Sienna', 'Silver', 'Skyblue', 'Slateblue', 'Slategray', 'Slategrey',
                'Snow', 'Springgreen', 'Steelblue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise',
                'Violet', 'Wheat', 'White', 'Whitesmoke', 'Yellow', 'Yellowgreen']

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#                    RCON Command Function                      #
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

def rcon_command(server_ip:str="1.1.1.1", server_port:int=0, rcon_password:str="12345", command:str="status"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)

    rcon_query = f"\xff\xff\xff\xffrcon {rcon_password} {command}".encode('latin1')

    server_address = (server_ip, server_port)
    try:
        sock.sendto(rcon_query, server_address)
        response, _ = sock.recvfrom(4096)
        s = response.decode('latin1')
        return splitstr("print", s)[1].strip()

    except socket.timeout:
        return "Failed to connect to server: Request timed out"
    except Exception as e:
        return f"Failed to connect to server: {e}"
    finally:
        sock.close()

def monotone(name:str):
	name = sub(r'\^\^([0-7]{2})|\^([0-7]{1})|\^', '', name)
	return name

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#                    Load Config Function                      #
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

def loadSavedServers(config_path:str):
    with open(config_path, 'r') as f:
        try:
            savedServers = json.load(f)
            return savedServers
        except json.decoder.JSONDecodeError:
            savedServers = {}
            savedServers["placeholder"] = {
                "ip": "1.1.1.1:28960",
                "rcon_pass": "12345"
            }
            saveServers(config_path, savedServers)
            return savedServers

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#                    Save Config Function                      #
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

def saveServers(config_path:str, sdict:dict):
    with open(config_path, 'w') as f:
        json.dump(sdict, f, indent=4)