folder("Whanos base images") {
	description("The base images of Whanos.")
}

folder("Projects") {
	description("The available projects in whanos.")
}

languages = ["befunge", "c", "java", "javascript", "python"]

for (int i = 0; i != 5; i++) {
	freeStyleJob("Whanos base images/whanos-${languages[i]}") {
		steps {
			shell("docker build $JENKINS_HOME/images/${languages[i]} -f $JENKINS_HOME/images/${languages[i]}/Dockerfile.base -t whanos-${languages[i]}")
		}
	}
}

freeStyleJob("Whanos base images/Build all base images") {
	publishers {
		downstream(
			languages.collect { language -> "Whanos base images/whanos-$language" }
		)
	}
}

freeStyleJob("link-project") {
	parameters {
		stringParam("REPOSITORY_URL", null, 'Repository url (e.g.: "git@github.com:USERNAME/PROJECT_NAME.git")')
		stringParam("PROJECT_NAME", null, null)
	}
	steps {
		dsl {
			text('''
				freeStyleJob("Projects/$PROJECT_NAME") {
					environmentVariables {
						env("PROJECT_NAME", "$PROJECT_NAME")
						keepSystemVariables(true)
					}
					scm {
						git {
							remote {
								name("origin")
								url("$REPOSITORY_URL")
								credentials("git_ssh_key")
							}
						}
					}
					triggers {
						scm("* * * * *")
					}
					wrappers {
						preBuildCleanup()
					}
					steps {
						shell('/usr/bin/python3.9 "$JENKINS_HOME/checker.py"')
					}
				}
			''')
		}
	}
}