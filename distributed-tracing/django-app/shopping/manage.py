#!/usr/bin/env python
import os
import sys


def remove_all_wavefront_env_prop(argv):
    print("Cleanup all the wavefront env properties before creating the wavefront client")
    if sys.argv[3].__eq__('direct'):
        if os.environ.get('WAVEFRONT_SERVER') is not None:
         del os.environ['WAVEFRONT_SERVER']
        if os.environ.get('WAVEFRONT_TOKEN') is not None :
         del os.environ['WAVEFRONT_TOKEN']
    elif sys.argv[3].__eq__('proxy'):
        if os.environ.get('PROXY_SERVER') is not None:
         del os.environ['PROXY_SERVER']
        if os.environ.get('PROXY_PORT') is not None :
         del os.environ['PROXY_PORT']


def set_direct_properties(argv):
    print("Direct InjectionKind")
    url = argv[4]
    token = argv[5]
    os.environ.setdefault('WAVEFRONT_SERVER', url)
    os.environ.setdefault('WAVEFRONT_TOKEN', token)
    print("setting wavefront client properties with direct injection")
    print('wavefront url set with : ' + os.environ.get('WAVEFRONT_SERVER') + ' env variable as : ' + 'WAVEFRONT_SERVER')
    print('wavefront token set with : ' + os.environ.get('WAVEFRONT_TOKEN') + ' env variable as : ' + 'WAVEFRONT_TOKEN')



def set_proxy_properties(argv):
    proxy = argv[4]
    port = argv[5]
    os.environ.setdefault('PROXY_SERVER', proxy)
    os.environ.setdefault('PROXY_PORT', port)
    print("setting wavefront client properties with proxy injection")
    print('proxy server set with : ' + os.environ.get('PROXY_SERVER') + ' env variable as  : ' + 'PROXY_SERVER')
    print('proxy port set with : ' + os.environ.get('PROXY_PORT') + ' env variable as  : ' + 'PROXY_PORT')
    """ java_home = os.environ.get('JAVA_HOME')
    print("JAVA_HOME:", java_home)
    proxy = os.environ.get('PROXY_SERVER')
    print(proxy) """


if __name__ == '__main__':
    remove_all_wavefront_env_prop(argv=sys.argv)
    injectionKind = sys.argv[3]
    if injectionKind.__eq__('direct'):
        set_direct_properties(argv=sys.argv)
    elif injectionKind.__eq__('proxy'):
        set_proxy_properties(argv=sys.argv)
    else:
        print("Kind should be direct or proxy injectionKind")
        raise Exception("wavefront client kind should be mentioned (direct or proxy) with properties")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopping.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    list = [sys.argv[0], sys.argv[1], sys.argv[2]]
    execute_from_command_line(argv=list)
