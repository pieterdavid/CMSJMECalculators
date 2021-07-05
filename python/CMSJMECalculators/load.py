def loadJMESystematicsCalculators():
    import os
    if "CMSSW_BASE" in os.environ:  # CMSSW/scram version
        import ROOT as gbl
        gbl.gSystem.Load("libUserCodeCMSJMECalculators")
        gbl.gROOT.ProcessLine('#define PROJECT_NAME "CMSSW"')
        gbl.gROOT.ProcessLine('#define CMSSW_GIT_HASH {}'.format(os.environ["CMSSW_GIT_HASH"]))
        gbl.gROOT.ProcessLine('#include "UserCode/CMSJMECalculators/interface/JMESystematicsCalculators.h"')
    else:
        import pkg_resources
        try:  # pip version
            dist_info = pkg_resources.get_distribution("CMSJMECalculators")
            incDir = pkg_resources.resource_filename("CMSJMECalculators", "include")
            libDir = pkg_resources.resource_filename("CMSJMECalculators", "lib")
            libName = "libCMSJMECalculators"
            import os.path
            import ROOT as gbl
            st = gbl.gSystem.Load(os.path.join(libDir, libName))
            if st == -1:
                raise RuntimeError("Library {0} could not be found".format(libName))
            elif st == -2:
                raise RuntimeError("Version match for library {0}".format(libName))
            gbl.gInterpreter.AddIncludePath(incDir)
            gbl.gROOT.ProcessLine('#include "JMESystematicsCalculators.h"')
        except pkg_resources.DistributionNotFound:  # fallback: load directly
            # TODO guess path from __file__ and add to dynamic path?
            libName = "libCMSJMECalculators"
            import ROOT as gbl
            st = gbl.gSystem.Load(libName)
            if st == -1:
                raise RuntimeError("Library {0} could not be found".format(libName))
            elif st == -2:
                raise RuntimeError("Version match for library {0}".format(libName))
    getattr(gbl, "JetVariationsCalculator::result_t")  # trigger dictionary generation
