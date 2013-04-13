include_recipe "apt::default"
include_recipe "python::default"


%w[
python-pygame
python-pyaudio
swig
python-dev
gcc
g++
libelf-dev
scons
arduino
].each do |pkg|
  package pkg do
    action :install
  end
end

%w[
pysimavr
pysimavrgui
].each do |pkg|
  python_pip pkg do
    action :install
  end
end



