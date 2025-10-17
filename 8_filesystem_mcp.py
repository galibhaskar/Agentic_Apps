from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("MyFileSystem")


# ================== tools ==================
@mcp.tool()
def addFile(path:str, filename:str) -> str:
    """Create a new file in the given path"""

    filepath = os.path.join(path, filename)

    if not os.path.exists(filepath):
        with open(filepath, 'w') as fp:
            fp.write("New file")
        
        print(f"File: {filename} is created")
 
    else:
        print(f"File already exists")

@mcp.tool()
def addFolder(path:str, dirname:str) -> str:
    """Create a new directory in the given path"""

    dirpath = os.path.join(path, dirname)
    
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        
        print(f"Directory with {dirname} is created")
    
    else:
        print(f"Directory already exists")


if __name__ == "__main__":
    mcp.run(transport="stdio")