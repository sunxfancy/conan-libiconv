
# conan-libiconv

[Conan.io](https://conan.io) package for libiconv library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/libiconv/1.14/sunxfancy/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py
    
## Upload packages to server

    $ conan upload libiconv/1.14@sunxfancy/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install libiconv/1.14@sunxfancy/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    libiconv/1.14@sunxfancy/stable

    [options]
    libiconv:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
