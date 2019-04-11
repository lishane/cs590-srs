import com.intellij.codeInspection.InspectionToolProvider;

public class DepreciatedAPIProvider implements InspectionToolProvider {
    public Class[] getInspectionClasses(){
        return new Class[]{DeprecatedAPIInspection.class};
    }

}
