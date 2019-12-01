run: Growth Hack Test
	task: 116
		name: Github Login
		sequence: >>>
		visit('https://github.com/')
		> xpath(//a[@href="/login"]).click()
		> xpath(//input[@type="text" and @name="login"]).type(example@gmail.com)
		> xpath(//input[@type="password" and @name="password"]).type(passcode)
		> xpath(//input[@type="submit" and @name="commit" and @value="Sign in"]).click()
		<<<
