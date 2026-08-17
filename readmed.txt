1.cmake: install 
安装项目到~/installTemp/myNetSrc/

2.cmake: run cpack
打包，生成rpm包，存储到build/packages路径

3.安装rpm包命令
sudo dnf localinstall grpc_demo-1.0.0-Linux.rpm 
安装到系统路径

sudo rpm -ivh --prefix /home/sola/customApp grpc_demo-1.0.0-Linux.rpm 
安装到个人路径

4.卸载rpm包命令(安装到哪个路径都能卸载)
sudo dnf remove grpc-demo