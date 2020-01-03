import cups

def print_photo(latest_photo):
    '''
    Connects to the photobooth and sends latest photo
    '''
    conn = cups.Connection ()
    printers = conn.getPrinters ()

    printer_name = list(printers.keys())[0]

    print (printer_name)

    conn.printFile('Canon_CP1000', latest_photo, "Photobooth", {})