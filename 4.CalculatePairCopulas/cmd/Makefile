#========================#
# Resource Path Settings #
#========================#
# Output Executable Name
PACKAGE_PATH := $(shell (cd ..; pwd))
PACKAGE_NAME := PairCopulaCalculator
TARGET       := $(PACKAGE_NAME).exe
EXECUTE_DIR  := ../exe

# Header files
HEADER_DIR := ../include
HEADERS    := $(shell ls $(HEADER_DIR))

# Source files
SRC_DIR  := ../src
MAIN_SRC := $(PACKAGE_NAME).cxx
SRCS	 := $(filter-out $(MAIN_SRC),$(shell ls $(SRC_DIR) | grep .cxx))

# Obj files
OBJ_DIR   := ../obj
MAIN_OBJ  := $(MAIN_SRC:%.cxx=%.o)
OBJS      := $(SRCS:%.cxx=%.o)

# Path for Search Files
vpath %.exe $(EXECUTE_DIR)/
vpath %.h   $(HEADER_DIR)/
vpath %.cxx $(SRC_DIR)/
vpath %.o   $(OBJ_DIR)/
VPATH = $(EXECUTE_DIR):$(HEADER_DIR):$(SRC_DIR):$(OBJ_DIR):.


#===========================#
# Compilation Flags Setting #
#===========================#
# Compile options
CFLAGS = -fPIC -pedantic -Wall -Wextra -std=c++14 -O3 

# Default Include Path & Library Link Options
INCFLAGS := -I$(HEADER_DIR) 
LIBS     := 

# Additional Include Path & Library Link Options
INCFLAGS += 
ifeq ($(shell uname),Linux)
	INCFLAGS += -I/usr/include/eigen3
else 
	INCFLAGS += -I/usr/local/include/eigen3
endif
LIBS     += -pthread


#================================#
# Compilation & Dependency Rules #
#================================#
all: $(TARGET)

$(TARGET) : $(MAIN_OBJ) $(OBJS)
	@mkdir -p $(EXECUTE_DIR)
	g++ $(CFLAGS) $(INCFLAGS) $(LIBS) \
	$(addprefix $(OBJ_DIR)/, $(MAIN_OBJ)) \
	$(addprefix $(OBJ_DIR)/, $(OBJS)) \
	-o $(addprefix $(EXECUTE_DIR)/, $(TARGET))

$(OBJS): %.o : %.cxx %.h
	@mkdir -p $(OBJ_DIR)
	g++ $(CFLAGS) $(INCFLAGS) -c $< -o $(OBJ_DIR)/$*.o

$(MAIN_OBJ): $(MAIN_SRC) $(OBJS)
	@mkdir -p $(OBJ_DIR)
	g++ $(CFLAGS) $(INCFLAGS) -c $(SRC_DIR)/$< -o $(OBJ_DIR)/$*.o


#========================#
# Other Utility Commands #
#========================#
.PHONY: all clean cleanall cleanobj cleanlib show

clean: cleanall

cleanall: cleanobj cleanlib

cleanobj:
	@rm -rf $(OBJ_DIR)

cleanlib: 
	@rm -rf $(EXECUTE_DIR)

show:
	@echo "pwd: $(PWD)"
	@echo "PACKAGE_NAME: $(PACKAGE_NAME)"
	@echo "HEADERS: $(HEADERS)"
	@echo "SRCS: $(SRCS)"
	@echo "INCFLAGS:" $(INCFLAGS)
