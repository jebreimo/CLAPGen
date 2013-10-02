import codegen
import os

class HppExpander(codegen.Expander):
    def __init__(self, members, className="Arguments",
                 fileName="ParseArguments.hpp",
                 functionName="parseArguments", namespace=""):
        codegen.Expander.__init__(self)
        self.className = className
        self.includeGuard = codegen.makeMacroName(fileName)
        self.functionName = functionName
        self.namespace = namespace.split("::")
        self.hasInfoOptions = any(m for m in members if m.type == "info")
        def isMandatory(m): return m.isOption and m.count == (1, 1)
        def isDefaultList(m): return m.type == "list" and m.default
        def isTrackable(m): return isMandatory(m) or isDefaultList(m)
        self.hasTrackedOptions = any(m for m in members if isTrackable(m))
        if not self.namespace[0]:
            self.namespace = []
        self._members = members

    def members(self, params, context):
        lines = []
        for m in self._members:
            if m.type != "final":
                if m.isOption:
                    lines.append("/** @brief Member for options: " + m.flags)
                else:
                    args = ", ".join(a.name for a in m.arguments)
                    lines.append("/** @brief Member for arguments: " + args)
                lines.append("  */")
                lines.append("%(memberType)s %(name)s;" % m)
        return lines

    def hasVectorMembers(self, params, context):
        for m in self._members:
            if m.type in ("list", "multivalue"):
                return True
        return False

    def hasStringMembers(self, params, context):
        for m in self._members:
            if m.valueType == "std::string":
                return True
        return False

    def beginNamespace(self, params, context):
        return "namespace " + " { namespace ".join(self.namespace) + " {"

    def endNamespace(self, params, context):
        return "}" * len(self.namespace)

def createFile(fileName, members, **kw):
    hppFile = os.path.join(os.path.dirname(__file__), "hpp_template.txt")
    hppTemplate = open(hppFile).read()
    kw["fileName"] = fileName
    open(fileName, "w").write(codegen.makeText(hppTemplate,
                                               HppExpander(members, **kw)))