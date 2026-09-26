"require-returns" requires useless return statements for return type "undefined"
Subject says it. If the return type is undefined I don't need a return statement in the code.

This plugin should concern itself with JSDoc &mdash; not with the code style! The return type when there is no `return` statement is `undefined`, so describing such a function as having `@returns {undefined}` is 100% correct. I should not get

    Present JSDoc @returns declaration but not available return expression in function  jsdoc/require-returns
