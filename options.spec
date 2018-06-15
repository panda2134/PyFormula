# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\Programming\\PyFormula'],
             binaries=[],
             datas=[
                ('pyformula.ini', 'pyformula.ini', 'DATA'),
                ('ui\\about.ui', 'ui\\about.ui', 'DATA'),
                ('ui\\main.ui', 'ui\\main.ui', 'DATA'),
                ('ui\\settings.ui', 'ui\\settings.ui', 'DATA'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='options',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='options')
