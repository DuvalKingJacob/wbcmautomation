"""Main Template File to pull the pieces together"""
from troposphere import Ref, If
from fanatics import Template, sgs
from fanatics.appstack import AppStack
from fanatics.params import default_params, instance_profile
from fanatics.conditions import ANY_DEV_CONDITION


def create_cft():
    """"Creates a Windows Instance for WBCM"""
    application = "WebBasedCommandManager"

    template = Template(
        description="Cloudformation for WBCM",
        application=application
    )
    app_stack = AppStack(
        service=application,
        vpc='services',
        ami='fanatics-webbased-cmd-mgr',
        subnet='app',
        security_groups=[
            If(
                ANY_DEV_CONDITION,
                sgs.REMOTE_LOGIN_SG,
                Ref("AWS::NoValue")
            ), "Tableau-SG", "APPSVC-NET-SG", "RedshiftAccess"],
        UseSignal=True
    )

    template.add_params(default_params + [instance_profile])
    app_stack.create_launch_config()
    app_stack.create_asg()
    template.add_resource(app_stack)
    return template


if __name__ == "__main__":
    print(create_cft().to_json())
