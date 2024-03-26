let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    # (pkgs.python3.withPackages (python-pkgs: [
    #   python-pkgs.numpy
    #   python-pkgs.torch
	  #   python-pkgs.torchvision2
    # ]))
    pkgs.python3
    pkgs.poetry
    pkgs.python3Packages.venvShellHook
    pkgs.autoPatchelfHook
  ];

  propagatedBuildInputs = [
    pkgs.stdenv.cc.cc.lib
  ];

  venvDir = "./venv";
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    pip install -U pip setuptools wheel
    pip install -r requirements.txt -r requirements-dev.txt
    pip install -e .
    autoPatchelf ./venv
  '';

  postShellHook = ''
  # set SOURCE_DATE_EPOCH so that we can use python wheels
  export SOURCE_DATE_EPOCH=315532800
  unset LD_LIBRARY_PATH
  '';
  preferLocalBuild = true;
}
