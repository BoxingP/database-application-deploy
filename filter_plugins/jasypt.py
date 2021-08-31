import os
import re
from subprocess import check_output, CalledProcessError, STDOUT
import shlex


def system_call(command):
    command = shlex.split(command)
    try:
        output = check_output(command, stderr=STDOUT).decode()
        success = True
    except CalledProcessError as e:
        output = e.output.decode()
        success = False
    return output, success


def get_file_path(file):
    return os.path.abspath(file)


def get_output(result):
    pattern = re.compile(r'^-.*OUTPUT-.*((?:\r?\n.*){2,3})', re.M)
    output = pattern.search(result)
    if output:
        output = str(output.group(1))
        pattern = re.compile(r'^\S.*$', re.M)
        output = pattern.search(output)
        return output.group()


def jasypt_encrypt(value, password, algorithm='PBEWITHHMACSHA512ANDAES_256', iterations=1000):
    jasypt_jar_path = get_file_path('filter_plugins/jasypt-1.9.3.jar')
    encrypt_command = '/usr/bin/java -cp ' + jasypt_jar_path + ' org.jasypt.intf.cli.JasyptPBEStringEncryptionCLI' \
                      + ' input=' + value + ' password=' + password + ' algorithm=' + algorithm \
                      + ' keyObtentionIterations=' + str(iterations) \
                      + ' saltGeneratorClassName=org.jasypt.salt.RandomSaltGenerator' \
                      + ' providerName=SunJCE stringOutputType=base64' \
                      + ' ivGeneratorClassName=org.jasypt.iv.RandomIvGenerator '
    result, status = system_call(encrypt_command)

    if status:
        return 'ENC(' + str(get_output(result)).strip() + ')'


def jasypt_decrypt(value, password, algorithm='PBEWITHHMACSHA512ANDAES_256', iterations=1000):
    value = str(re.search(r'\((.*?)\)', value).group(1))
    jasypt_jar_path = get_file_path('filter_plugins/jasypt-1.9.3.jar')
    encrypt_command = '/usr/bin/java -cp ' + jasypt_jar_path + ' org.jasypt.intf.cli.JasyptPBEStringDecryptionCLI' \
                      + ' input=' + value + ' password=' + password + ' algorithm=' + algorithm \
                      + ' keyObtentionIterations=' + str(iterations) \
                      + ' saltGeneratorClassName=org.jasypt.salt.RandomSaltGenerator' \
                      + ' providerName=SunJCE stringOutputType=base64' \
                      + ' ivGeneratorClassName=org.jasypt.iv.RandomIvGenerator '
    result, status = system_call(encrypt_command)

    if status:
        return str(get_output(result)).strip()


class FilterModule(object):

    def filters(self):
        return {
            'jasypt_encrypt': jasypt_encrypt,
            'jasypt_decrypt': jasypt_decrypt
        }
