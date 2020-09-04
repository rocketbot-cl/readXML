# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""
from bs4 import BeautifulSoup
import os

base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'readXML' + os.sep + 'libs' + os.sep
sys.path.append(cur_path)
import xmltodict
import json

global to_dict
global GetText

def GetText(nodo):
    try:
        return nodo.text
    except:
        return ""


"""
    Obtengo el modulo que fue invocado
"""
module = GetParams("module")

"""
    Obtengo variables
"""
if module == "getDataXML":

    path = GetParams('path')
    var_ = GetParams('result')
    print(var_)

    try:
        xml = open(path, "r").read()
        bs = BeautifulSoup(xml, "lxml")
        # print(bs)
    except:
        PrintException()

    try:

        """DATOS FACTURA"""

        tipoDTE = GetText(bs.tipodte)
        folio = GetText(bs.folio)
        fchEmision = GetText(bs.fchemis)

        """DATOS EMISOR"""

        RutEmisor = GetText(bs.emisor.rutemisor)
        RznSocEmisor = GetText(bs.emisor.rznsoc)
        GiroEmisor = GetText(bs.emisor.giroemis)
        ActecoEmisor = GetText(bs.emisor.acteco)
        DirEmisor = GetText(bs.emisor.dirorigen)
        CmnaEmisor = GetText(bs.emisor.cmnaorigen)
        CiudadEmisor = GetText(bs.emisor.ciudadorigen)

        """DATOS RECEPTOR"""

        RutReceptor = GetText(bs.receptor.rutrecep)
        RznSocReceptor = GetText(bs.receptor.rznsocrecep)
        GiroReceptor = GetText(bs.receptor.girorecep)
        ContactoReceptor = GetText(bs.receptor.contacto)
        DirReceptor = GetText(bs.receptor.dirrecep)
        CmnaReceptor = GetText(bs.receptor.cmnarecep)
        CiudadReceptor = GetText(bs.receptor.ciudadrecep)

        """TOTALES"""

        MontoNeto = GetText(bs.totales.mntneto)
        MontoExe = GetText(bs.totales.mntexe)
        TasaIva = GetText(bs.totales.tasaiva)
        Iva = GetText(bs.totales.iva)
        MontoTotal = GetText(bs.mnttotal)

        """DETALLE"""

        Itemdetalle = []
        detalles = bs.find_all('detalle')

        for detalle in detalles:
            tmp = \
                {
                    "Producto": GetText(detalle.nmbitem),
                    "Cantidad": GetText(detalle.qtyitem),
                    "Precio": GetText(detalle.prcitem),
                    "Monto": GetText(detalle.montoitem)
                }
            Itemdetalle.append(tmp)

        datos = {'tipoDTE': tipoDTE, 'folio': folio, 'fchEmision': fchEmision, 'RutEmisor': RutEmisor,
                 'RznSocEmisor': RznSocEmisor,
                 'GiroEmisor': GiroEmisor, 'ActecoEmisor': ActecoEmisor, 'DirEmisor': DirEmisor,
                 'CmnaEmisor': CmnaEmisor, 'CiudadEmisor': CiudadEmisor,
                 'RutReceptor': RutReceptor, 'RznSocReceptor': RznSocReceptor, 'GiroReceptor': GiroReceptor,
                 'ContactoReceptor': ContactoReceptor, 'DirReceptor': DirReceptor,
                 'CmnaReceptor': CmnaReceptor, 'CiudadReceptor': CiudadReceptor, 'MontoNeto': MontoNeto,
                 'MontoExe': MontoExe,
                 'TasaIva': TasaIva, 'Iva': Iva, 'MontoTotal': MontoTotal, 'Detalles': Itemdetalle}
        # print(datos)

        SetVar(var_, datos)

    except:
        PrintException()

if module == "ColFactura":

    path = GetParams('path')
    var_ = GetParams('result')

    try:
        with open(path, "r", encoding="utf8") as file:
            xml = file.read()
        bs = BeautifulSoup(xml, "lxml")
        # print(bs)
    except:
        PrintException()
        raise e


    try:
        """DATOS FACTURA"""

        # tipoDTE = GetText(bs.tipodte)
        # folio = GetText(bs.folio)
        # fchEmision = GetText(bs.fchemis)

        """DATOS EMISOR"""
        print("holaaaa")
        invoice = bs.attachment["cac:externalreference"]["cbc:description"]["invoice"]

        invoice_child = invoice.findChild("cac:accountingsupplierparty")

        RznSocEmisor = GetText(invoice_child.find("cac:partyname").find("cbc:name"))
        address = invoice_child.find("cac:physicallocation").find("cac:address")
        IDEmisor = GetText(address.find("cbc:id"))
        ContactEmisor = GetText(invoice_child.find("cbc:telephone"))
        DirEmisor = GetText(address.find("cbc:line"))
        CiudadEmisor = GetText(address.find("cbc:cityname"))

        """DATOS RECEPTOR"""

        # RutReceptor = GetText(bs.receptor.rutrecep)
        # RznSocReceptor = GetText(bs.receptor.rznsocrecep)
        # GiroReceptor = GetText(bs.receptor.girorecep)
        # ContactoReceptor = GetText(bs.receptor.contacto)
        # DirReceptor = GetText(bs.receptor.dirrecep)
        # CmnaReceptor = GetText(bs.receptor.cmnarecep)
        # CiudadReceptor = GetText(bs.receptor.ciudadrecep)

        """TOTALES"""

        MontoNeto = GetText(invoice.find("cac:legalmonetarytotal").find("cbc:lineextensionamount"))
        # MontoExe = GetText(bs.totales.mntexe)
        # TasaIva = GetText(bs.totales.tasaiva)
        # Iva = GetText(bs.totales.iva)
        MontoTotal = GetText(invoice.find("cac:legalmonetarytotal").find("cbc:payableamount"))

        """DETALLE"""

        item_detail = []
        invoice_line = invoice.findAll('cac:invoiceline')

        for line in invoice_line:

            tmp = \
                {
                    "codigo": GetText(line.find("cac:item").find("cac:standarditemidentification").find("cbc:id")),
                    "description": GetText(line.find("cac:item").find("cbc:description")),
                    "Cantidad": GetText(line.find("cac:price").find("cbc:basequantity")),
                    "Monto": GetText(line.find("cac:price").find("cbc:priceamount"))

                }
            item_detail.append(tmp)

        datos = {'razonSocial': RznSocEmisor,
                 'id': IDEmisor, 'contacto': ContactEmisor, 'direccion': DirEmisor,
                 'ciudad': CiudadEmisor, 'montoNeto': MontoNeto, 'montoTotal': MontoTotal, 'detalles': item_detail}

        SetVar(var_, datos)

    except Exception as e:
        PrintException()
        raise e


if module == "EcuFactura":

    path = GetParams('path')
    var_ = GetParams('result')

    try:
        with open(path, "r", encoding="utf8") as file:
            xml = file.read()
        bs = BeautifulSoup(xml, "lxml")
    except:
        PrintException()
        raise e


    try:
        """DATOS FACTURA"""

        estado = GetText(bs.estado)
        numero_autorizacion = GetText(bs.numeroautorizacion)
        fecha_autorizacion = GetText(bs.fechaautorizacion)
        ambiente = GetText(bs.ambiente)

        """FACTURA"""

        factura = bs.comprobante.factura

        informacion_tributaria = {
            "razon_social": GetText(factura.infotributaria.razonsocial),
            "nombre_comercial":  GetText(factura.infotributaria.nombrecomercial),
            "ruc":  GetText(factura.infotributaria.ruc),
            "secuencial":  GetText(factura.infotributaria.secuencial),
            "direccion":  GetText(factura.infotributaria.dirmatriz)

        }

        info_factura = {
            "fecha_emision": GetText(factura.infofactura.fechaemision),
            "direccion": GetText(factura.infofactura.direstablecimiento),
            "razon_social": GetText(factura.infofactura.razonsocialcomprador),
            "total_sin_impuestos": GetText(factura.infofactura.totalsinimpuestos),
        }
        total_con_impuestos = factura.infofactura.totalsinimpuestos.find_all('totalimpuesto')
        total_impuesto = []
        for impuesto in total_con_impuestos:
            total_impuesto.append({
                "base_imponible": GetText(impuesto.baseimponible),
                "valor": GetText(impuesto.valor)
            })

        info_factura["total_con_impuestos"] = total_impuesto


        """DETALLE"""

        detalles = []

        item_detail = factura.detalles.find_all('detalle')

        for detalle in item_detail:
            print(detalle, type(detalle), "\n*************")
            tmp = {
                "codigo_principal": GetText(detalle.codigoprincipal),
                "codigo_auxiliar": GetText(detalle.codigoauxiliar),
                "descripcion": GetText(detalle.descripcion),
                "cantidad": GetText(detalle.cantidad),
                "precio_unitario": GetText(detalle.preciounitario),
                "descuento": GetText(detalle.descuento),
                "precio_total_sin_impuesto": GetText(detalle.precio_total_sin_impuesto)
            }

            impuestos = []
            for impuesto in detalle.impuestos.find_all('impuesto'):
                impuestos.append({
                    "tarifa": GetText(impuesto.tarifa),
                    "base_imponible": GetText(impuesto.baseimponible),
                    "valor": GetText(impuesto.valor)
                })
            tmp["impuestos"] = impuestos
            detalles.append(tmp)




        datos = {
            "estado": estado,
            "numero_autorizacion": numero_autorizacion,
            "fecha_autorizacion": fecha_autorizacion,
            "ambiente": ambiente,
            "informacion_tributaria": informacion_tributaria,
            "info_factura": info_factura,
            "detalles": detalles,
        }

        SetVar(var_, datos)

    except Exception as e:
        PrintException()
        raise e

if module == "xml2Dict":
    path = GetParams('path')
    var_ = GetParams('result')

    try:
        with open(path, encoding='utf-8') as fd:
            doc = xmltodict.parse(fd.read())
            # doc = eval(str(json.dumps(doc)).replace("null", '""').replace("false", "False").replace("true", "True"))
        SetVar(var_, json.loads(json.dumps(doc)))
    except Exception as e:
        PrintException()
        raise e


if module == "xml_str2Dict":
    xml = GetParams('xml')
    result = GetParams('result')

    try:
        doc = xmltodict.parse(xml)
        SetVar(result, json.dumps(doc))
    except Exception as e:
        PrintException()
        raise e