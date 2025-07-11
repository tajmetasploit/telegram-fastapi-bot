{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.sqlite
    pkgs.postgresql
    pkgs.uvicorn
    pkgs.python310Packages.pip
    pkgs.python310Packages.setuptools
    pkgs.python310Packages.wheel
  ];
}
