def loadJMESystematicsCalculators():
    import os
    import pkg_resources
    import ROOT as gbl
    try:  # pip version
        pkg_resources.get_distribution("CMSJMECalculators")
        incDir = pkg_resources.resource_filename("CMSJMECalculators", "include")
        libDir = pkg_resources.resource_filename("CMSJMECalculators", "lib")
        libName = "libCMSJMECalculators"
        import os.path
        st = gbl.gSystem.Load(os.path.join(libDir, libName))
        if st == -1:
            raise RuntimeError("Library {0} could not be found".format(libName))
        elif st == -2:
            raise RuntimeError("Version match for library {0}".format(libName))
        gbl.gInterpreter.AddIncludePath(incDir)
        gbl.gROOT.ProcessLine('#include "JMESystematicsCalculators.h"')
    except pkg_resources.DistributionNotFound as ex:  # fallback: load directly
        libName = "libCMSJMECalculatorsDict"
        gbl.gSystem.AddDynamicPath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        st = gbl.gSystem.Load(libName)
        if st == -1:
            raise RuntimeError("Library {0} could not be found".format(libName))
        elif st == -2:
            raise RuntimeError("Version match for library {0}".format(libName))
    getattr(gbl, "JetVariationsCalculator::result_t")  # trigger dictionary generation (if needed)
