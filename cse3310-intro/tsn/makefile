OSPL_LIBS = -lpthread -lddskernel -ldcpssacpp
LIBS=-L${OSPL_HOME}/lib ${OSPL_LIBS}

CFLAGS = -Wall -O0 -g -I. \
         -I./include -I${OSPL_HOME}/include/dcps/C++/SACPP \
         -I${OSPL_HOME}/include/sys \
         -I${OSPL_HOME}/include

CXXFLAGS = -std=c++11

all: tsn


IDL_GENERATED_H= \
                 ccpp_tsn.h \
                 tsnDcps.h \
                 tsnDcps_impl.h \
                 tsn.h \
                 tsnSplDcps.h

IDL_GENERATED_CPP=\
                 tsn.cpp \
                 tsnDcps.cpp \
                 tsnDcps_impl.cpp \
                 tsnSplDcps.cpp

IDL_GENERATED=${IDL_GENERATED_H} ${IDL_GENERATED_CPP}

${IDL_GENERATED}: idl/tsn.idl
	${OSPL_HOME}/bin/idlpp -l cpp idl/tsn.idl

COMMON_CPP= src/CheckStatus.cpp src/DDSEntityManager.cpp

COMMON_H= src/dds_io.h src/CheckStatus.h src/DDSEntityManager.h src/tsnCommunication.h src/tsnGlobalVars.h src/tsnHeader.h src/tsnGUI.h

tsn: ${IDL_GENERATED_H} ${IDL_GENERATED_CPP} src/tsnMain.cpp ${COMMON_CPP} ${COMMON_H}
	g++ -o $@ ${CFLAGS} ${CXXFLAGS} $^ ${LIBS} -lncurses
	clear
	@echo "use ./tsn to execute. Make sure current window is at least 80x43"
clean:
	-rm -f stalker tsn
	-rm -f ${IDL_GENERATED_H} ${IDL_GENERATED_CPP}
	-rm -f ospl-error.log ospl-info.log
