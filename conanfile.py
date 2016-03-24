from conans import ConanFile
import os, shutil
from conans.tools import download, unzip, replace_in_file, check_md5
from conans import CMake


class LibiconvConan(ConanFile):
    name = "libiconv"
    version = "1.14"
    branch = "master"
    ZIP_FOLDER_NAME = "libiconv-%s" % version
    generators = "cmake"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url = "http://github.com/lasote/conan-libiconv"
    #requires = "zlib/1.2.8@lasote/stable"

    def source(self):
        if self.settings.os != "Windows": # wraps winiconv for windows
            zip_name = "libiconv-%s.tar.gz" % self.version
            download("http://ftp.gnu.org/pub/gnu/libiconv/%s" % zip_name, zip_name)
            check_md5(zip_name, "e34509b1623cec449dfeb73d7ce9c6c6")
            unzip(zip_name)
            os.unlink(zip_name)
            if self.settings.os == "Linux":
	        text_to_replace = '_GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");'
                replaced_text = '''#if defined(__GLIBC__) && !defined(__UCLIBC__) && !__GLIBC_PREREQ(2, 16)
    _GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
    #endif'''
                replace_in_file(os.path.join(self.ZIP_FOLDER_NAME, "srclib", "stdio.in.h"), text_to_replace, replaced_text)
            
    def config(self):
        try: # Try catch can be removed when conan 0.8 is released
            del self.settings.compiler.libcxx 
        except: 
            pass
        if self.settings.os == "Windows":
            self.requires.add("winiconv/1.14.0@lasote/stable", private=False)
        
    def generic_env_configure_vars(self, verbose=False):
        """Reusable in any lib with configure!!"""
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            libs = 'LIBS="%s"' % " ".join(["-l%s" % lib for lib in self.deps_cpp_info.libs])
            ldflags = 'LDFLAGS="%s"' % " ".join(["-L%s" % lib for lib in self.deps_cpp_info.lib_paths]) 
            archflag = "-m32" if self.settings.arch == "x86" else ""
            cflags = 'CFLAGS="-fPIC %s %s"' % (archflag, " ".join(self.deps_cpp_info.cflags))
            cpp_flags = 'CPPFLAGS="%s %s"' % (archflag, " ".join(self.deps_cpp_info.cppflags))
            command = "env %s %s %s %s" % (libs, ldflags, cflags, cpp_flags)
        elif self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            cl_args = " ".join(['/I"%s"' % lib for lib in self.deps_cpp_info.include_paths])
            lib_paths= ";".join(['"%s"' % lib for lib in self.deps_cpp_info.lib_paths])
            command = "SET LIB=%s;%%LIB%% && SET CL=%s" % (lib_paths, cl_args)
            if verbose:
                command += " && SET LINK=/VERBOSE"
        
        return command
       
    def build(self):
        if self.settings.os == "Windows":
            pass # wrapper for winiconv
        else:
            self.build_with_configure()
            
        
    def build_with_configure(self): 
        configure_command = "cd %s && %s ./configure --enable-static --enable-shared --disable-rpath" % (self.ZIP_FOLDER_NAME, 
                                                         self.generic_env_configure_vars())
        self.output.warn(configure_command)
        self.run(configure_command)
        self.run("cd %s && make" % self.ZIP_FOLDER_NAME)
       

    def package(self):
        self.copy("*.h", "include", "%s/include" % (self.ZIP_FOLDER_NAME), keep_path=True)
        if self.options.shared:
            self.copy(pattern="*.so*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(pattern="*.dll*", dst="bin", src=self.ZIP_FOLDER_NAME, keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src="%s" % self.ZIP_FOLDER_NAME, keep_path=False)
        
        self.copy(pattern="*.lib", dst="lib", src="%s" % self.ZIP_FOLDER_NAME, keep_path=False)
        
    def package_info(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.cpp_info.libs = ['charset', 'iconv']
            if self.settings.os == "Linux" or (self.options.shared and self.settings.os == "Macos"):
                self.cpp_info.defines.append("LIBICONV_PLUG=1")


