Failed due to duplicate Message-ID header
I've been using this project for a while and it's awesome, thanks a lot! I stumbled upon an error for the first time today. Error log from CloudWatch is below:

```
2017-05-03T11:38:51.802Z	f2ab5592-2ff4-11e7-97ca-a1db4277fedb	{ level: 'error',
message: 'sendRawEmail() returned error.',
error: 
{ [InvalidParameterValue: Duplicate header 'Message-ID'.]
message: 'Duplicate header \'Message-ID\'.',
code: 'InvalidParameterValue',
time: Wed May 03 2017 11:38:51 GMT+0000 (UTC),
requestId: '14956f7e-2ff5-11e7-8290-6fdc1cb44eda',
statusCode: 400,
retryable: false,
retryDelay: 16.828257404267788 },
stack: 'InvalidParameterValue: Duplicate header \'Message-ID\'.\n at Request.extractError (/var/runtime/node_modules/aws-sdk/lib/protocol/query.js:47:29)\n at Request.callListeners (/var/runtime/node_modules/aws-sdk/lib/sequential_executor.js:105:20)\n at Request.emit (/var/runtime/node_modules/aws-sdk/lib/sequential_executor.js:77:10)\n at Request.emit (/var/runtime/node_modules/aws-sdk/lib/request.js:673:14)\n at Request.transition (/var/runtime/node_modules/aws-sdk/lib/request.js:22:10)\n at AcceptorStateMachine.runTo (/var/runtime/node_modules/aws-sdk/lib/state_machine.js:14:12)\n at /var/runtime/node_modules/aws-sdk/lib/state_machine.js:26:10\n at Request.<anonymous> (/var/runtime/node_modules/aws-sdk/lib/request.js:38:9)\n at Request.<anonymous> (/var/runtime/node_modules/aws-sdk/lib/request.js:675:12)\n at Request.callListeners (/var/runtime/node_modules/aws-sdk/lib/sequential_executor.js:115:18)' }
```

Repro step: create a Skype account using foobar@mydomain.com. The email containing the verification code fails to be forwarded.
