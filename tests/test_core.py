import importlib.util
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'packages/core/src'))
from cycling_suite.credentials import Secrets,account
from cycling_suite.transports import FolderTransport,safe_name,validate_url
from cycling_suite.instance import InstanceLock

class CoreTests(unittest.TestCase):
    def test_vault_namespace_injection_and_no_plaintext_fallback(self):
        class Vault:
            def __init__(self):self.values={}
            def get_password(self,service,key):return self.values.get((service,key))
            def set_password(self,service,key,value):self.values[service,key]=value
            def delete_password(self,service,key):del self.values[service,key]
        vault=Vault();a=Secrets('AppA',lambda:vault);b=Secrets('AppB',lambda:vault)
        a.save('same-root','secret');self.assertIsNone(b.read('same-root'));self.assertEqual(a.read('same-root'),'secret');a.delete('same-root');self.assertIsNone(a.read('same-root'))
        def blocked():raise RuntimeError('private diagnostic')
        with self.assertRaisesRegex(ValueError,'Portachiavi'):Secrets('AppA',blocked).save('key','secret')

    def test_immutable_folder_isolation_traversal_and_instance_lock(self):
        with TemporaryDirectory() as temporary:
            root=Path(temporary);folder=root/'exchange';folder.mkdir();store=root/'data'
            a=FolderTransport(folder,'channel',store,prefix='app-a');b=FolderTransport(folder,'channel',store,prefix='app-b')
            self.assertTrue(a.put('one.bin',b'data'));self.assertFalse(a.put('one.bin',b'data'));self.assertEqual(b.list(),[])
            with self.assertRaises(ValueError):a.put('one.bin',b'different')
            with self.assertRaises(ValueError):a.get('../outside')
            with self.assertRaises(ValueError):FolderTransport(folder,'bad/../channel',store)
            lock=InstanceLock(store)
            try:
                with self.assertRaises(ValueError):InstanceLock(store)
            finally:lock.close()
            InstanceLock(store).close()

    def test_delivery_is_deterministic_and_preserves_source_and_license(self):
        spec=importlib.util.spec_from_file_location('sync_core',ROOT/'scripts/sync-core.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        first=module.contents();self.assertEqual(first,module.contents())
        import io,zipfile
        with zipfile.ZipFile(io.BytesIO(first)) as wheel:
            self.assertIn('cycling_suite/desktop.py',wheel.namelist())
            self.assertTrue(any(name.endswith('/LICENSE') for name in wheel.namelist()))
        for value in ('http://example.invalid/','https://user:pass@example.invalid/','https://example.invalid/../secrets'):
            with self.assertRaises(ValueError):validate_url(value)

if __name__=='__main__':unittest.main()
