import com.intellij.codeInsight.daemon.GroupNames;
import com.intellij.codeInspection.*;
import com.intellij.execution.filters.TextConsoleBuilderFactory;
import com.intellij.execution.ui.ConsoleView;
import com.intellij.execution.ui.ConsoleViewContentType;
import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.wm.ToolWindow;
import com.intellij.openapi.wm.ToolWindowManager;
import com.intellij.psi.*;
import com.intellij.psi.tree.IElementType;
import com.intellij.ui.DocumentAdapter;
import com.intellij.ui.content.Content;
import com.intellij.util.IncorrectOperationException;
import org.jetbrains.annotations.*;

import javax.swing.*;
import javax.swing.event.DocumentEvent;
import java.awt.*;
import java.util.StringTokenizer;


// Modified example from here:
// https://github.com/JetBrains/intellij-sdk-docs/blob/master/code_samples/comparing_references_inspection/source/com/intellij/codeInspection/ComparingReferencesInspection.java
//
// Other useful(?) links:
// https://www.jetbrains.org/intellij/sdk/docs/tutorials/code_inspections.html
// https://www.jetbrains.org/intellij/sdk/docs/basics/architectural_overview/navigating_psi.html

public class DeprecatedAPIInspection extends AbstractBaseJavaLocalInspectionTool {
    // Setup logger?
    private static final Logger LOG = Logger.getInstance("#com.intellij.codeInspection.DeprecatedAPIInspectionInspection");

    // Declare quickfix method
    private final LocalQuickFix myQuickFix = new MyQuickFix();
    @SuppressWarnings({"WeakerAccess"})
    @NonNls
    // Not sure here, no mention in docs
    // Only check within these classes? Doesn't make sense
    public String CHECKED_CLASSES = "java.lang.String;java.util.Date";
    @NonNls


    /* // This is not working, something about an invalid property key. Commented out for now
    private static final String DESCRIPTION_TEMPLATE =
            InspectionsBundle.message("inspection.comparing.references.problem.descriptor");
    */
    @NotNull
    public String getDisplayName() {

        return "Search for deprecated Android API Calls";
    }

    @NotNull
    public String getGroupDisplayName() {
        return GroupNames.BUGS_GROUP_NAME;
    }

    @NotNull
    public String getShortName() {
        return "DeprecatedAPIInspection";
    }

    private boolean isCheckedType(PsiType type) {
        if (!(type instanceof PsiClassType)) return false;

        StringTokenizer tokenizer = new StringTokenizer(CHECKED_CLASSES, ";");
        while (tokenizer.hasMoreTokens()) {
            String className = tokenizer.nextToken();
            if (type.equalsToText(className)) return true;
        }

        return false;
    }

    // Visitor node, part of the main logic
    // Need to find how to elegantly read from one of the mapping files
    // Which mapping file is the one we want to use? Should prob read and preprocess
    @NotNull
    @Override
    public PsiElementVisitor buildVisitor(@NotNull final ProblemsHolder holder, boolean isOnTheFly) {
        return new JavaElementVisitor() {

            @Override
            public void visitReferenceExpression(PsiReferenceExpression psiReferenceExpression) {
            }


            // Two potential calls, need exploring
            @Override
            public void visitCallExpression(PsiCallExpression callExpression) {
                super.visitCallExpression(callExpression);
            }

            @Override
            public void visitElement(PsiElement element) {
                super.visitElement(element);
            }

            @Override
            public void visitMethod(PsiMethod method) {
                super.visitMethod(method);
                ToolWindow toolWindow = ToolWindowManager.getInstance(method.getProject()).getToolWindow("MyPlugin");
                ConsoleView consoleView = TextConsoleBuilderFactory.getInstance().createBuilder(method.getProject()).getConsole();
                Content content = toolWindow.getContentManager().getFactory().createContent(consoleView.getComponent(), "MyPlugin Output", false);
                toolWindow.getContentManager().addContent(content);
                consoleView.print("Hello from MyPlugin!", ConsoleViewContentType.NORMAL_OUTPUT);

                method.getName();
            }

            // Old method call, keeping for example, need to delete
            @Override
            public void visitBinaryExpression(PsiBinaryExpression expression) {
                super.visitBinaryExpression(expression);
                IElementType opSign = expression.getOperationTokenType();
                if (opSign == JavaTokenType.EQEQ || opSign == JavaTokenType.NE) {
                    PsiExpression lOperand = expression.getLOperand();
                    PsiExpression rOperand = expression.getROperand();
                    if (rOperand == null || isNullLiteral(lOperand) || isNullLiteral(rOperand)) return;

                    PsiType lType = lOperand.getType();
                    PsiType rType = rOperand.getType();

                    // Uses Description template from
                    if (isCheckedType(lType) || isCheckedType(rType)) {
                        holder.registerProblem(expression,
                                "placeholder",/*DESCRIPTION_TEMPLATE,*/ myQuickFix);
                    }
                }
            }
        };
    }

    private static boolean isNullLiteral(PsiExpression expr) {
        return expr instanceof PsiLiteralExpression && "null".equals(expr.getText());
    }

    // Unmodified, TODO after visitor is fixed
    private static class MyQuickFix implements LocalQuickFix {
        @NotNull
        public String getName() {
            // The test (see the TestThisPlugin class) uses this string to identify the quick fix action.
            return InspectionsBundle.message("inspection.comparing.references.use.quickfix");
        }


        public void applyFix(@NotNull Project project, @NotNull ProblemDescriptor descriptor) {
            try {
                PsiBinaryExpression binaryExpression = (PsiBinaryExpression) descriptor.getPsiElement();
                IElementType opSign = binaryExpression.getOperationTokenType();
                PsiExpression lExpr = binaryExpression.getLOperand();
                PsiExpression rExpr = binaryExpression.getROperand();
                if (rExpr == null)
                    return;

                PsiElementFactory factory = JavaPsiFacade.getInstance(project).getElementFactory();
                PsiMethodCallExpression equalsCall =
                        (PsiMethodCallExpression) factory.createExpressionFromText("a.equals(b)", null);

                equalsCall.getMethodExpression().getQualifierExpression().replace(lExpr);
                equalsCall.getArgumentList().getExpressions()[0].replace(rExpr);

                PsiExpression result = (PsiExpression) binaryExpression.replace(equalsCall);

                if (opSign == JavaTokenType.NE) {
                    PsiPrefixExpression negation = (PsiPrefixExpression) factory.createExpressionFromText("!a", null);
                    negation.getOperand().replace(result);
                    result.replace(negation);
                }
            } catch (IncorrectOperationException e) {
                LOG.error(e);
            }
        }

        @NotNull
        public String getFamilyName() {
            return getName();
        }
    }

    // Options TODO fix or remove
    public JComponent createOptionsPanel() {
        JPanel panel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        final JTextField checkedClasses = new JTextField(CHECKED_CLASSES);
        checkedClasses.getDocument().addDocumentListener(new DocumentAdapter() {
            public void textChanged(DocumentEvent event) {
                CHECKED_CLASSES = checkedClasses.getText();
            }
        });

        panel.add(checkedClasses);
        return panel;
    }

    // Enable extension by default
    public boolean isEnabledByDefault() {
        return true;
    }
}