import OnboardingWidget from '../../../../../frappe/frappe/public/js/frappe/widgets/onboarding_widget.js'

class MyOnboardingWidget extends OnboardingWidget {
	show_step(step){
		step.description = __(step.description);
		step.title = __(step.title);
    	super.show_step(step);
	}
}

frappe.widget.widget_factory.onboarding = MyOnboardingWidget
