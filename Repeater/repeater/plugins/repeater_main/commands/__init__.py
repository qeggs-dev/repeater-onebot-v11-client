from ..import_assist import SubmoduleImporter as _ImportPublicPkgs

_importer= _ImportPublicPkgs()
_importer.import_pkgs()
_importer.inject_modules()
__all__ = _importer.all_list() # type: ignore