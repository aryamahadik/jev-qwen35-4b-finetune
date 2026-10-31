"""T66 MSG production commit-message pool: SOURCE of pools/msg_messages.json (Claude-authored; one template per line; `{slot}` fields).

Kinds: the eight realised change kinds (CH-1, CH-2, CH-3, CH-5, CH-6, CH-8, CH-9, CH-10; CH-4 and CH-7 are never realised, see msg_spec.py) and the three trivial hunk kinds
(fmt, comment, doc). Per kind two styles: I = names the changed function / values (uses {fn} ...), N = identifier-free intent (no slot at all).
Rules the lint (lint_msg_pool.py) enforces: a template names its own kind (verb + object) and no other kind's; no normalised text is shared between kinds; token Jaccard of
two templates of different kinds < 0.5; >= 40 templates per kind; slots only from the kind's own set (msg_spec.KIND_SLOTS).
Rebuild the JSON:  python3 -m T66.msg_pool_src   (from c21_fam/; rewrites pools/msg_messages.json; the dev / dev2 halves are fixed by a seeded hash, msg_pool.py).
"""
import os
import sys

SRC = r"""
## CH-1 I
add a guard against negative {arg} in {fn}
fix: reject negative {arg} in {fn}
{fn}: validate that {arg} is not negative
validate that {arg} is non-negative before {fn} does any work
guard {fn} against negative input
add a guard to {fn} that raises ValueError for negative {arg}
add a guard on negative {arg} in {fn}()
feat({fn}): guard against negative {arg}
add input validation to {fn}: reject negative {arg}
reject negative values at the start of {fn}
add a precondition check on {arg} in `{fn}`: not negative
sanity check {arg} first thing in {fn}: negative is rejected
stop negative {arg} reaching the arithmetic in {fn} with a guard
guard: raise ValueError("{word}") for negative {arg} in {fn}
add a negative-input guard to {fn} raising "{word}"
{fn} now validates {arg} and rejects negative values
protect {fn} with a guard clause for negative {arg}
validation for {fn}: no negative {arg}
refuse negative {arg} in {fn}: add a guard clause
defensive guard in {fn}: {arg} must not be negative
add early validation of {arg} to {fn}, negative values are rejected
guard clause in {fn} rejects negative {arg} with "{word}"
check {arg} in {fn} and reject it if negative
add a guard: negative {arg} raises ValueError in {fn}
{fn}(): add guard for negative {arg}
fix: {fn} accepted negative {arg}, add validation
validate {arg} in `{fn}`: negative input is an error
add a check in {fn} that rejects negative {arg}
## CH-1 N
add a guard that rejects negative input
add a guard check that raises ValueError for negative input
validate the input is non-negative before computing
guard clause for negative input
add an early guard for negative numbers
guard against negative input with a ValueError
reject negative values up front
fix: reject negative input with a ValueError
add input validation: reject negative values
add a precondition that the argument is not negative
stop negative numbers flowing into the calculation with a guard
sanity check the argument and reject negative values
feat: validate that the value is non-negative
add a guard for negative values, raising ValueError
add a guard check: negative numbers raise ValueError
add a guard: if the value is < 0, raise ValueError
add a negative-input guard clause
validate input and reject negative values
accept only non-negative input: add a validation check
fix: add a guard so negative values do not get through
protect the calculation from negative input with a guard
add a guard: no negative numbers allowed
guard: negative values raise ValueError
refuse negative input: add a guard
add a ValueError guard for negative input
early validation: negative values are rejected
guard clause for negative numbers
add validation that rejects values < 0
## CH-2 I
{fn}: one more loop pass to fix the off-by-one
fix off-by-one in {fn}: loop needs one more pass
fix off-by-one in {fn}: range({arg} + 1), one more pass
`{fn}` uses range({arg} + 1) for the last pass: off-by-one
{fn}: for {lv} in range({arg} + 1), fix off-by-one
off-by-one in {fn}: {lv} must reach range({arg} + 1)
off-by-one: {fn} loops {lv} over range({arg} + 1), last value
fix off-by-one in {fn}: loop over range({arg} + 1)
{fn}: range({arg}) missed the last value, an off-by-one
fix off-by-one at the {fn} range end, one more pass
off-by-one in {fn}: last pass of {lv} missing
fix off-by-one: {fn} range must include the last {arg}
fix off-by-one in {fn} loop range, one more pass
{fn}: range stopped one short of the last {arg}, off-by-one
chore: fix loop off-by-one in {fn}, one more pass
fix: off-by-one in {fn} range, last pass skipped
{fn} loop skipped its last pass: off-by-one fixed
off-by-one fix in the {fn} loop: run the last pass
fix off-by-one in {fn}: loop range({arg} + 1) once more
bug: {fn} skipped the last pass, off-by-one fixed
fix the off-by-one error in {fn}, one more pass
{fn}: off-by-one in the range, last value included
off-by-one: range({arg}) -> range({arg} + 1) in {fn}
fix off-by-one in {fn}: {lv} reaches the last value
{fn}: range was short by one, off-by-one fixed
fix off-by-one in {fn}: run {lv} one more time
{fn} range end off-by-one fixed: last pass now runs
fix off-by-one in {fn}: iterate range({arg} + 1)
## CH-2 N
one more loop pass to fix the off-by-one
fix the off-by-one: the loop needs one more pass
fix off-by-one: add + 1 to the range end
fix off-by-one: range + 1 reaches the last value
range end off-by-one: add 1 to reach the last value
fix the off-by-one in the range end, one more pass
fix off-by-one: the range must include its last value
off-by-one: the range stopped one short, add 1
fix off-by-one in the loop range, one more pass
fix off-by-one: the last loop pass was missing
the loop skipped its last pass, fix the off-by-one
fix off-by-one: run one more loop pass
off-by-one fix: loop one more time over the range
chore: fix the loop off-by-one, one more pass
fix the off-by-one in the loop, last pass included
correct the off-by-one in the loop: one more pass
bug: the last loop pass never ran, off-by-one fixed
off-by-one in the loop range, fixed with one more pass
fix off-by-one: the loop reaches the last index
range + 1: fix the off-by-one, one more pass
fix off-by-one in the loop: run the last pass
range was short by one: off-by-one fixed
fix off-by-one: iterate the range plus one more pass
off-by-one: loop to the last value of the range
fix off-by-one: the loop stopped one pass short
add 1 to the range end: off-by-one fixed
fix off-by-one: extend the range by one more pass
the last value was never reached: off-by-one
## CH-3 I
rename {fn} to {new_fn}
refactor: rename `{fn}` -> `{new_fn}`
rename {fn}: it is now called {new_fn}
rename {fn} to a clearer name, {new_fn}
rename function {fn} as {new_fn}
Rename {fn}() to {new_fn}() for clarity
rename {fn} and use the name {new_fn} from now on
rename {fn} so it reads better ({new_fn})
{fn} -> {new_fn} (rename)
refactor({fn}): rename to {new_fn}
rename the helper {fn} to {new_fn}
rename {fn} to a better name: {new_fn}
rename: {new_fn} replaces {fn}
renamed {fn} to {new_fn}
refactor: rename `{fn}`, new name `{new_fn}`
rename: {fn} => {new_fn}
rename {fn} to a more descriptive {new_fn}
rename {fn}, it deserves a proper name: {new_fn}
rename {fn} to {new_fn} to match the naming convention
rename {fn} to {new_fn} (update the name)
rename public function {fn}, new name is {new_fn}
rename {fn} over to {new_fn}
rename the function {fn}; it is {new_fn} from now on
chore: rename {fn} to a better name ({new_fn})
rename {fn}: new name {new_fn}
rename {fn} (now {new_fn})
refactor: rename {fn}, it becomes {new_fn}
rename {fn} to something clearer: {new_fn}
## CH-3 N
rename the function to something more descriptive
rename the helper to a clearer name
refactor: rename function for clarity
rename the function to match the naming convention
rename the function to a better name
rename the public function in the module
rename function to a more meaningful name
rename: the function has a new name
rename the function with a descriptive name
rename: clearer function name
refactor: rename the function, better naming
renamed the function for readability
rename for consistency with the other helpers
rename the function so its name is self-explanatory
chore: rename the function to follow naming rules
rename the function, its name was misleading
rename it to something that says what it does
rename to switch to a clearer function name
rename this function to a proper name
rename the function in this module
rename the function after what it computes
rename the helper function
rename with a new, shorter name for the function
rename to avoid the confusing old name
refactor: rename for better naming
rename to improve the function's name
rename function; the old name was unclear
rename the function to adopt a clearer name
## CH-5 I
change the default of {param} from {num_old} to {num_new} in {fn}
set the default {param} to {num_new} in `{fn}`
let {param} default to {num_new} in `{fn}`
change default argument {param} of {fn} to {num_new}
make {num_new} the default {param} for {fn}
change {fn} defaults: {param} = {num_new}
update {fn} so {param} defaults to {num_new} rather than {num_old}
increase the default for {param} in {fn} to {num_new}
{param} now defaults to {num_new} in {fn}
change the default for {param} in {fn}: {num_old} -> {num_new}
set {param}'s default to {num_new} (it was {num_old}) in {fn}
{fn}: default for {param} is now {num_new} (was {num_old})
use {num_new} as the default for {param} in {fn} instead of {num_old}
change the default value of {param} in {fn} to {num_new}
update the default of {param} in {fn} to {num_new}
bump {param}'s default to {num_new} in {fn}
fix: wrong default for {param} in {fn}, set it to {num_new}
config: set the {param} default to {num_new} in {fn}
change the default of the {param} argument of {fn} to {num_new}
set a new default for {param} in {fn}: {num_new}
tune the default of {param} in {fn} to {num_new}
{fn}: change the default {param} from {num_old} to {num_new}
default {param} for {fn} changed to {num_new}
set default {param}={num_new} in {fn}
adjust the default {param} in {fn} ({num_old} -> {num_new})
change the default {param} to {num_new} (was {num_old}), {fn}
update default of the {param} argument of {fn} to {num_new}
when {param} is omitted, {fn} should use the default {num_new}
## CH-5 N
change the default from {num_old} to {num_new}
set the default to {num_new} instead of {num_old}
bump the default to {num_new}
the default is {num_new} now (was {num_old})
change the default of the optional argument to {num_new}
update the default argument: {num_old} -> {num_new}
change the default to {num_new} when the argument is omitted
set a bigger default, {num_new} instead of {num_old}
change the default to {num_new}, the old one was wrong
change the default to {num_new} for the argument
change the default used when the caller omits the argument: {num_new}
bump the argument's default to {num_new}
change what the argument defaults to: {num_new}
set the default argument to {num_new} (it was {num_old})
change the argument's default from {num_old} to {num_new}
bump the default argument up to {num_new}
update the default to {num_new}
tune the default: {num_old} -> {num_new}
change the default to {num_new} when no argument is passed
set the default to {num_new}, the old one was {num_old}
change the fallback default for the argument to {num_new}
use {num_new} as the argument's default
argument default changed to {num_new}
update the argument's default from {num_old} to {num_new}
change the default offset to {num_new}
adjust the default argument to {num_new}
set the default argument to {num_new}, bigger than before
update the default that omitted arguments get to {num_new}
## CH-6 I
make {param} a required parameter of {fn}
make {param} a mandatory parameter of {fn}
{param} must be supplied to {fn}: required parameter
{param} must be supplied to {fn} now: it is a required parameter
fix: {fn} must get {param} passed in explicitly, make it a required parameter
stop assuming {num_old} for {param} in {fn}: it is a required parameter
make {param} required, a mandatory parameter of {fn}
required parameter: {param} in {fn}
mandatory parameter: {param} in {fn}
{param} is a required parameter of {fn} now
{param} is a mandatory parameter of {fn} now
make {param} a required parameter in {fn} instead of falling back to {num_old}
{fn}: make {param} a required parameter, callers supply it explicitly
{param} becomes a required parameter for {fn}
{fn} makes {param} a required parameter for every caller
{fn}: {param} is now a required parameter, callers must supply it
fix: make {param} a required parameter of {fn}, passed in explicitly
stop assuming {num_old} for {param}: required parameter of {fn}
{param} must be passed to {fn} explicitly: it is a mandatory parameter
make {param} a required parameter of {fn}, no fallback to {num_old}
{fn}({arg}, {param}): {param} is a required parameter now
{param} in {fn} must be supplied by callers: a required parameter
callers must supply {param} to {fn}: required parameter
{param} is now a mandatory parameter in {fn}, supplied by the caller
the {fn} signature makes {param} a required parameter
{fn} signature: {param} is a required parameter now
make {param} a required parameter, not a fallback, in {fn}
mark {param} as a required parameter of {fn}
## CH-6 N
make the parameter a required parameter
make the parameter a mandatory parameter
the parameter must be supplied: required parameter
the extra parameter is now a required parameter
make the extra argument a required parameter so callers must supply it
fix: callers must supply the value, make it a required parameter
stop assuming a value for the parameter: it is a required parameter
mandatory parameter: callers must supply it
required parameter: the caller must supply it
the parameter is a required parameter now
the second parameter is now a mandatory parameter
make the second argument a required parameter
the extra argument becomes a required parameter
make the argument a mandatory parameter for callers
callers must supply the argument: it is a required parameter
no fallback value now: required parameter
the signature now has a required parameter
make the new parameter a required parameter in the signature
the argument must be passed in explicitly: required parameter
required parameter: nothing is assumed for the value
make the extra parameter a mandatory parameter
the extra parameter must be supplied by callers, a required parameter
change the signature so the parameter is a required parameter
the argument is a mandatory parameter now
fix: the caller relied on a hidden value, make it a required parameter
the second parameter is a required parameter now, supplied by the caller
make the argument a required parameter, callers supply it explicitly
mandatory parameter instead of an assumed value
## CH-8 I
better error message for {fn}: "{word_new}" instead of "{word_old}"
{fn} error message wording: "{word_old}" becomes "{word_new}"
improve the {fn} error message: "{word_old}" becomes "{word_new}"
more helpful error message for {fn}: "{word_new}" replaces "{word_old}"
rephrase the {fn} error message: "{word_new}" (was "{word_old}")
fix the ValueError message in {fn}: "{word_new}", not "{word_old}"
make the {fn} error message read "{word_new}", not "{word_old}"
change the error message in {fn} from "{word_old}" to "{word_new}"
reword the {fn} error message text to "{word_new}" (was "{word_old}")
update {fn} error message: "{word_old}" now reads "{word_new}"
update the {fn} exception message, "{word_old}" is now "{word_new}"
use "{word_new}" as the {fn} error message, not "{word_old}"
misleading error message in {fn}: "{word_old}" is now "{word_new}"
new wording for the {fn} error message: "{word_new}" (was "{word_old}")
{fn}: the error message now reads "{word_new}" rather than "{word_old}"
the {fn} failure message should say "{word_new}", not "{word_old}"
change the ValueError message of {fn}: "{word_old}" -> "{word_new}"
reword ValueError message in {fn}: "{word_old}" -> "{word_new}"
{fn}: error message "{word_old}" -> "{word_new}"
error message of {fn} reworded: "{word_old}" -> "{word_new}"
replace the {fn} error message "{word_old}" with "{word_new}"
polish the {fn} error message: "{word_new}" instead of "{word_old}"
improve the {fn} failure message: "{word_old}" becomes "{word_new}"
change the {fn} error text from "{word_old}" to "{word_new}"
{fn} error text now says "{word_new}" instead of "{word_old}"
better wording for the {fn} error message: "{word_new}" (was "{word_old}")
fix: misleading {fn} error message, "{word_old}" becomes "{word_new}"
update the {fn} error wording: "{word_old}" replaced by "{word_new}"
## CH-8 N
change the error message for the failure case
improve the wording of the error message
the error message was reworded for the failure case
new error message for the failure case
swap the error message text for a clearer one
better error message when the check fails
polish the error message so it reads better
make the error message clearer
reword the error text so it reads better
the failure message now says something different
rephrase the failure message for the failure case
update the error message wording
fix: misleading error message
replace the error text when the check fails
change the error message text
reword the error message
rephrase the error message so it reads better
improve the error message for the failure case
update the error message when the check fails
replace the error message
the error message was misleading, change it
better wording for the error message
new wording for the error text
the error message is reworded for the failure case
change the failure message text
improve the failure message wording
reword the failure message when the check fails
update the error text wording
## CH-9 I
add a logging call for {tok} in {fn}
add logging to {fn}: record {tok}
log {tok} in {fn} with a new logging call
{fn}: add a log line that records {tok}
add a log statement for {tok} to {fn}
feat({fn}): add logging of {tok}
insert a logging call in {fn} for {tok}
add a log call to {fn} recording {tok}
add logging in {fn} so {tok} shows up in the logs
log the {tok} step in {fn}
add a trace log for {tok} in `{fn}`
{fn}: new log entry for {tok}
add a debug log of {tok} to {fn}
add a logger call to {fn} that logs {tok}
chore: add logging for {tok} in {fn}
record {tok} in the log from {fn}
add a log record for {tok} in {fn}
log a {tok} event from {fn}
add a logging statement to {fn} for {tok}
have {fn} log {tok}
{fn} now logs {tok}
add log tracing of {tok} to {fn}
emit a log for {tok} in {fn}
add a logging call to {fn}, logging {tok}
log {tok} in `{fn}`
add logging of the {tok} step to {fn}
add a log marker for {tok} in {fn}
log the {tok} case in {fn} with an extra logging call
## CH-9 N
add a logging call to the function
add logging to the function
log the step with a new logging call
add a log line for the new step
add a log statement to the function
feat: add logging to the code path
insert a logging call in the function body
add a log call that records the step
add logging so the step shows up in the logs
log the step in the function
add a trace log to the function
new log entry for the step
add a debug log of the step
add a logger call that logs the step
chore: add logging for the new step
record the step in the log
add a log record for the step
log an event from the function
add a logging statement to the function body
have the function log the step
the function now logs the step
add log tracing to the function
emit a log for the step
add a logging call, logging the step
log the new step in the function
add logging of the extra step
add a log marker for the step
log the extra case with an additional logging call
## CH-10 I
scale by {num_new} instead of {num_old} in {fn}
{fn} multiplies by {num_new} now; the old multiplier was {num_old}
constant bumped to {num_new} in `{fn}`
{fn} should multiply by {num_new}, not {num_old}
coefficient of {fn} increased to {num_new}
change the scaling constant of {fn}: {num_old} becomes {num_new}
{fn} had the wrong multiplier, set it to {num_new}
change the factor applied by {fn} ({num_old} -> {num_new})
{fn} now uses the multiplier {num_new}
adjust the scale constant used in {fn}
update magic number {num_old} in {fn} to {num_new}
make {fn} scale {arg} by a bigger factor ({num_new})
exchange multiplier {num_old} for {num_new} inside {fn}
retune the scaling in {fn}
{fn}: new multiplier constant {num_new}
set the constant factor of {fn} to {num_new}
tweak the multiplier for {arg} in {fn}
magic number in {fn} goes {num_old} to {num_new}
scale {arg} {num_new}x in {fn} instead of {num_old}x
the factor in `{fn}` was too small, use {num_new}
{fn}: replace the {num_old}x multiplier with {num_new}x
increase the scaling constant in {fn} from {num_old}
change the multiplication constant used by {fn}
{fn} scales {arg} by the constant {num_new} from now on
use a bigger constant when scaling {arg} in {fn}
{fn} used the wrong factor ({num_old}); it is {num_new}
tune {fn}: factor {num_old}, now {num_new}
correct the scaling factor to {num_new} in {fn}
## CH-10 N
change the scale factor
increase the multiplier used on the input
use a larger constant for scaling
tweak the scaling coefficient
fix: wrong multiplier, use a bigger factor
update the magic number used for scaling
retune the scale constant
bump the constant factor applied to the input
make the coefficient bigger
the scaling factor was too small, adjust it
adjust the multiplier applied to the value
swap the constant used to scale the input
tune the scaling constant
switch to a new multiplier value
correct the scale factor
chore: change the constant multiplier
scale the value by a different factor
increase the coefficient applied to the input
replace the multiplication constant
multiply by a larger constant
update the scale constant
the factor used for scaling changed
choose a better multiplier
set a bigger scaling constant
adjust the constant used in the first step
recalibrate the scale factor
update the coefficient used for scaling
use a different multiplier
## fmt I
{fn}: reformat the lines
{fn}: reformat the operators
{fn}: reformat the arithmetic
{fn}: reformat the operations
{fn}: reformat the statements
{fn}: reformat the assignments
{fn}: reformat the expressions
{fn}: reformat the calculations
{fn}: reformat only the lines
{fn}: reformat the stage lines
{fn}: chore: reformat the lines
{fn}: style: reformat the lines
{fn}: reformat only the arithmetic
{fn}: style: reformat the operations
{fn}: style: reformat the calculations
{fn}: reformat the arithmetic expressions
{fn}: formatting: reformat the expressions
{fn}: formatting: reformat the calculations
reformat only the lines in {fn}
reformat only the lines of {fn}
reformat only the lines for {fn}
chore: reformat the lines in {fn}
chore: reformat the lines of {fn}
chore: reformat the lines for {fn}
reformat only the operations of {fn}
reformat only the assignments for {fn}
chore: reformat the expressions for {fn}
{fn}: formatting: reformat the stage lines
{fn}: formatting cleanup of the calculations
{fn}: reformat the assignments formatting only
{fn}: reformat the lines in one pass
reformat only the stage lines in {fn}
reformat only the stage lines of {fn}
{fn}: reformat and clean up the lines
style pass: reformat the lines of {fn}
{fn}: reformat the operators in one pass
{fn}: reformat and clean up the operations
reformat and compact the assignments for {fn}
reformat and normalize the calculations in {fn}
{fn}: style: reformat the operators cosmetic only
{fn}: reformat the arithmetic lines for consistency
{fn}: reformat and compact the arithmetic expressions
{fn}: formatting: reformat the statements cosmetic only
{fn}: formatting: reformat the arithmetic for consistency
reformat and clean up the lines in {fn}
reformat and clean up the lines of {fn}
reformat and clean up the lines for {fn}
{fn}: reformat only the lines in one pass
{fn}: clean up the formatting of the lines
reformat and clean up the lines inside {fn}
{fn}: reformat the lines to keep lines compact
{fn}: touch up the formatting of the assignments
reformat only the operations for {fn} cosmetic only
reformat only the calculations in {fn} formatting only
reformat only the assignments within {fn} formatting only
{fn}: formatting: reformat the assignments per the formatter
{fn}: reformat the calculations spaces around operators removed
{fn}: formatting: reformat the arithmetic expressions cosmetic only
reformat only the lines in {fn} in one pass
reformat only the lines of {fn} in one pass
reformat only the lines for {fn} in one pass
touch up the formatting of the lines in {fn}
reformat and clean up the stage lines in {fn}
reformat only the operations in {fn} in one pass
chore: reformat the statements of {fn} in one pass
{fn}: reformat and compact the operators in one pass
style pass: reformat the lines of {fn} formatting only
reformat only the stage lines inside {fn} formatting only
chore: reformat the assignments within {fn} across the file
formatting cleanup of the operations for {fn} formatting only
style pass: reformat the assignments inside {fn} for consistency
chore: reformat the arithmetic expressions of {fn} formatting only
reformat only the stage lines in {fn} in one pass
reformat only the stage lines of {fn} in one pass
{fn}: reformat and clean up the lines in one pass
reformat and compact the lines in {fn} in one pass
{fn}: reformat and clean up the lines across the file
style pass: reformat the expressions of {fn} in one pass
{fn}: touch up the formatting of the lines for consistency
{fn}: reformat only the stage lines dropping the extra spaces
reformat and clean up the operations within {fn} for consistency
{fn}: style pass: reformat the statements dropping the extra spaces
chore: reformat the lines inside {fn} spaces around operators removed
reformat and normalize the arithmetic expressions for {fn} cosmetic only
reformat and clean up the lines in {fn} in one pass
reformat and clean up the lines of {fn} in one pass
{fn}: clean up the formatting of the lines in one pass
reformat and clean up the statements of {fn} in one pass
style pass: reformat the lines in {fn} as agreed in review
reformat and compact the lines for {fn} to keep lines compact
touch up the formatting of the operators for {fn} cosmetic only
{fn}: reformat and compact the statements to match the style guide
reformat and compact the lines inside {fn} dropping the extra spaces
reformat and normalize the arithmetic inside {fn} to keep lines compact
clean up the formatting of the lines in {fn} in one pass
touch up the formatting of the lines of {fn} in one pass
reformat and clean up the stage lines for {fn} in one pass
clean up the formatting of the operators for {fn} in one pass
clean up the formatting of the lines for {fn} per the formatter
touch up the formatting of the assignments inside {fn} in one pass
formatting cleanup of the stage lines within {fn} so they read evenly
formatting cleanup of the calculations for {fn} to match the style guide
clean up the formatting of the lines of {fn} to keep lines compact
reformat and clean up the operators for {fn} to match the style guide
clean up the formatting of the statements of {fn} to keep lines compact
{fn}: clean up the formatting of the calculations to match the style guide
reformat and clean up the lines inside {fn} using the compact operator style
touch up the formatting of the arithmetic expressions in {fn} per the formatter
## fmt N
reformat only the lines
chore: reformat the lines
reformat only the operators
reformat only the arithmetic
reformat only the operations
reformat only the statements
chore: reformat the arithmetic
chore: reformat the assignments
reformat only the stage lines
reformat and compact the lines
style pass: reformat the lines
chore: reformat the stage lines
formatting cleanup of the lines
reformat and normalize the lines
reformat only the arithmetic lines
formatting cleanup of the arithmetic
reformat and normalize the calculations
reformat only the arithmetic expressions
reformat and clean up the lines
reformat and clean up the operators
reformat and clean up the arithmetic
reformat and clean up the operations
reformat and clean up the statements
reformat and compact the stage lines
style pass: reformat the stage lines
reformat and clean up the expressions
reformat only the lines for consistency
chore: reformat the lines formatting only
reformat only the operations formatting only
chore: reformat the arithmetic formatting only
reformat only the lines in one pass
clean up the formatting of the lines
touch up the formatting of the lines
chore: reformat the lines in one pass
reformat and clean up the stage lines
reformat only the lines across the file
reformat only the operators in one pass
reformat only the operations in one pass
clean up the formatting of the expressions
reformat only the operations across the file
chore: reformat the operators per the formatter
style pass: reformat the statements cosmetic only
style pass: reformat the arithmetic for consistency
reformat and normalize the operations for consistency
reformat only the stage lines in one pass
clean up the formatting of the stage lines
reformat and compact the lines in one pass
style pass: reformat the lines in one pass
touch up the formatting of the stage lines
reformat only the lines as agreed in review
reformat only the lines so they read evenly
reformat and normalize the lines in one pass
reformat and compact the lines across the file
reformat and compact the assignments in one pass
chore: reformat the arithmetic so they read evenly
chore: reformat the calculations as agreed in review
reformat and clean up the calculations for consistency
formatting cleanup of the arithmetic lines cosmetic only
reformat and clean up the lines in one pass
reformat and clean up the lines across the file
reformat and clean up the operators in one pass
reformat and clean up the operations in one pass
reformat and compact the stage lines in one pass
reformat only the lines to match the style guide
style pass: reformat the stage lines in one pass
reformat and clean up the lines per the formatter
chore: reformat the lines to match the style guide
clean up the formatting of the lines for consistency
reformat and clean up the operators per the formatter
formatting cleanup of the operators so they read evenly
formatting cleanup of the statements as agreed in review
formatting cleanup of the operations to keep lines compact
clean up the formatting of the lines in one pass
touch up the formatting of the lines in one pass
reformat and clean up the stage lines in one pass
reformat and clean up the lines as agreed in review
reformat and clean up the lines so they read evenly
clean up the formatting of the lines across the file
clean up the formatting of the operators in one pass
clean up the formatting of the calculations in one pass
touch up the formatting of the statements across the file
reformat and compact the arithmetic to match the style guide
reformat and compact the stage lines dropping the extra spaces
reformat and normalize the arithmetic lines to keep lines compact
clean up the formatting of the stage lines in one pass
touch up the formatting of the stage lines in one pass
clean up the formatting of the lines as agreed in review
touch up the formatting of the lines as agreed in review
clean up the formatting of the lines to keep lines compact
reformat and clean up the operations to match the style guide
reformat and clean up the stage lines dropping the extra spaces
reformat and compact the arithmetic lines to match the style guide
clean up the formatting of the assignments dropping the extra spaces
touch up the formatting of the arithmetic expressions per the formatter
clean up the formatting of the operators to match the style guide
clean up the formatting of the statements to match the style guide
clean up the formatting of the stage lines dropping the extra spaces
reformat and clean up the stage lines with no blanks around operators
reformat and clean up the stage lines using the compact operator style
touch up the formatting of the operators with no blanks around operators
clean up the formatting of the arithmetic expressions so they read evenly
clean up the formatting of the stage lines without spaces around operators
clean up the formatting of the stage lines to match the style guide
touch up the formatting of the stage lines to match the style guide
clean up the formatting of the arithmetic lines to match the style guide
touch up the formatting of the arithmetic lines to match the style guide
clean up the formatting of the stage lines with no blanks around operators
touch up the formatting of the stage lines with no blanks around operators
## comment I
{fn}: add a comment
{fn}: put a comment
{fn}: write a comment
{fn}: comment the code
{fn}: put a comment here
{fn}: write a comment here
write a comment before {fn}
{fn}: comment the code here
{fn}: write a comment first
comment the code before {fn}
{fn}: add a one-line comment
{fn}: add a reminder comment
{fn}: comment the code first
{fn}: add a maintenance comment
{fn}: add a comment for it
{fn}: put a comment for it
put a comment ahead of {fn}
write a comment ahead of {fn}
{fn}: add a header comment here
add a reminder comment above {fn}
add a reminder comment before {fn}
{fn}: comment the code for context
add a maintenance comment above {fn}
{fn}: add a maintenance comment here
add a maintenance comment before {fn}
{fn}: add a maintenance comment first
write a comment on top of {fn}
{fn}: add a brief comment for it
{fn}: add a plain comment above it
write a comment above {fn} for later
{fn}: add a one-line comment before it
comment the code before {fn} for context
{fn}: comment the code before the release
{fn}: write a comment above the definition
{fn}: write a comment for new contributors
{fn}: add a maintenance comment for context
{fn}: comment the code above the definition
{fn}: comment the code for new contributors
{fn}: write a comment before the definition
{fn}: comment the code before the definition
add a new comment on top of {fn}
add a note comment on top of {fn}
{fn}: add a note as a comment here
add a comment ahead of {fn} for later
{fn}: add a reminder comment with a note
{fn}: insert a comment line first for later
{fn}: insert a comment line before the release
{fn}: comment the code here for new contributors
{fn}: add a maintenance comment above the function
{fn}: add a maintenance comment before the release
{fn}: comment the code for the infrastructure team
{fn}: add a maintenance comment above the definition
{fn}: add a maintenance comment for new contributors
{fn}: add a maintenance comment before the definition
add a note as a comment next to {fn}
{fn}: add a note as a comment above it
add a new comment ahead of {fn} for later
{fn}: add a plain comment first with a note
{fn}: add a plain comment to mark the release
add a comment line before {fn} for the reviewers
{fn}: add a maintenance comment up front for later
{fn}: add a plain comment first for new contributors
{fn}: add a header comment for the infrastructure team
add a maintenance comment above {fn} for new contributors
{fn}: add a maintenance comment here for new contributors
add a maintenance comment before {fn} for new contributors
{fn}: add a maintenance comment first for new contributors
{fn}: add a maintenance comment for the infrastructure team
put a comment in front of {fn} with a note
add a brief comment ahead of {fn} with a note
add a note as a comment before {fn} for context
{fn}: add a comment for it for the next maintainer
{fn}: add a note comment above the function for later
{fn}: add a reminder comment for it for new contributors
{fn}: add a comment line before the definition for context
{fn}: add a maintenance comment first for the next maintainer
{fn}: add a maintenance comment here for the infrastructure team
{fn}: add a maintenance comment before the definition for context
{fn}: add a maintenance comment first for the infrastructure team
{fn}: comment the code before the definition for new contributors
add a note as a comment above {fn} as a reminder
add a note comment above {fn} so the owner is clear
{fn}: add a comment for it that points to the runbook
{fn}: add a plain comment next to the function for later
add a brief comment before {fn} that points to the runbook
{fn}: write a comment ahead of the function for the reviewers
{fn}: add a brief comment above the function before the release
{fn}: put a comment above the function for the infrastructure team
{fn}: add a maintenance comment above it for the infrastructure team
{fn}: add a maintenance comment above the function for new contributors
add a new comment next to {fn} so the owner is clear
{fn}: add a new comment just before the def with a note
{fn}: add a note comment for it that points to the runbook
{fn}: put a comment ahead of the function to mark the release
{fn}: add a one-line comment up front for whoever reads it next
{fn}: add a plain comment just before the def for new contributors
{fn}: insert a comment line before the definition to mark the release
{fn}: add a maintenance comment above the definition to mark the release
{fn}: write a comment in front of the function to mark the release
{fn}: add a note comment over the function that points to the runbook
{fn}: insert a comment line in front of the function before the release
{fn}: insert a comment line above the definition for whoever reads it next
{fn}: add a one-line comment above the definition that points to the runbook
{fn}: add a maintenance comment above the definition that points to the runbook
## comment N
write a comment here
comment the code here
insert a comment line
write a comment first
add a one-line comment
add a reminder comment
comment the code first
add a maintenance comment
put a comment for it
add a new comment here
write a comment above it
insert a comment line here
add a one-line comment here
add a one-line comment first
add a reminder comment first
comment the code for context
add a maintenance comment here
add a maintenance comment first
add a note as a comment
add a new comment for it
add a new comment up front
insert a comment line for it
add a header comment for later
add a reminder comment before it
put a comment before the definition
add a maintenance comment for context
comment the code above the definition
comment the code for new contributors
write a comment before the definition
comment the code before the definition
add a note as a comment here
add a new comment with a note
add a note as a comment first
add a comment saying who to ask
add a header comment as a reminder
comment the code first as a reminder
put a comment first before the release
put a comment first for new contributors
insert a comment line above the definition
add a reminder comment before the definition
comment the code for the infrastructure team
add a maintenance comment above the definition
add a maintenance comment for new contributors
add a maintenance comment before the definition
add a note as a comment for it
add a note as a comment above it
add a note as a comment before it
add a note comment for it for later
comment the code for it as a reminder
add a header comment up front for later
put a comment before it for the reviewers
add a header comment for the next maintainer
add a one-line comment here before the release
insert a comment line first for new contributors
comment the code first for the infrastructure team
add a maintenance comment here for new contributors
add a maintenance comment first for new contributors
add a maintenance comment for the infrastructure team
put a comment for it saying who to ask
add a comment up front saying who to ask
add a comment before it saying who to ask
add a header comment on top of the function
add a comment next to the function for later
add a comment above the definition with a note
add a plain comment over the function for later
add a one-line comment above it for the reviewers
add a reminder comment before it for the reviewers
add a comment above the definition for the reviewers
add a plain comment before the definition for context
add a reminder comment above the definition for context
comment the code above the definition before the release
write a comment before the definition for new contributors
add a note as a comment for it for later
add a note as a comment here with a note
add a note as a comment here as a reminder
add a note comment above it saying who to ask
add a comment ahead of the function with a note
add a comment line here that points to the runbook
write a comment above the function saying who to ask
add a new comment above the function before the release
add a header comment above it for the infrastructure team
add a reminder comment above the function before the release
add a reminder comment before the definition for the reviewers
comment the code above the definition for the infrastructure team
add a brief comment for it so the owner is clear
add a note comment on top of the function for later
add a comment line up front for whoever reads it next
add a reminder comment just before the def as a reminder
add a reminder comment ahead of the function as a reminder
write a comment ahead of the function for the next maintainer
add a comment ahead of the function for the infrastructure team
add a maintenance comment just before the def for new contributors
add a note comment before the definition for the infrastructure team
add a reminder comment above the definition for the infrastructure team
add a note comment above the definition for whoever reads it next
add a one-line comment in front of the function before the release
add a brief comment next to the function for the infrastructure team
insert a comment line just before the def for the infrastructure team
add a maintenance comment next to the function for the next maintainer
add a maintenance comment in front of the function for new contributors
add a maintenance comment just before the def for the infrastructure team
add a maintenance comment before the definition that points to the runbook
add a maintenance comment next to the function so the owner is clear
add a one-line comment just before the def that points to the runbook
add a new comment in front of the function for the infrastructure team
add a one-line comment next to the function that points to the runbook
add a note comment in front of the function for the infrastructure team
insert a comment line on top of the function for the infrastructure team
## doc I
{fn}: add a docstring
docstring added to {fn}
{fn}: write a docstring
docstring added for {fn}
{fn}: attach a docstring
{fn}: insert a docstring
{fn}: docstring added now
{fn}: include a docstring
add a docstring for {fn}
insert a docstring to {fn}
write a docstring inside {fn}
{fn}: add a one-line docstring
include a docstring inside {fn}
{fn}: add the missing docstring
{fn}: include a docstring first
{fn}: write a one-line docstring
{fn}: attach a one-line docstring
{fn}: docstring added for readers
add a new docstring to {fn}
{fn}: add a docstring to it
add a new docstring for {fn}
{fn}: add a new docstring now
{fn}: add a new docstring first
{fn}: add a brief docstring first
{fn}: write a one-line docstring now
{fn}: docstring added noting the owner
{fn}: docstring added before the release
{fn}: docstring added inside the function
{fn}: docstring added for new contributors
{fn}: docstring added for later maintainers
{fn}: add a new docstring to it
{fn}: add a new docstring for it
{fn}: add a brief docstring for it
add a docstring for {fn} for readers
{fn}: insert a docstring in the module
{fn}: insert a docstring to the function
{fn}: write a docstring before the release
{fn}: include a docstring inside the function
{fn}: docstring added now for later maintainers
docstring added inside {fn} for new contributors
{fn}: docstring added here for later maintainers
docstring added inside {fn} for later maintainers
{fn}: docstring added first for later maintainers
{fn}: docstring added for the infrastructure team
add a docstring at the start of {fn}
add a docstring to {fn} in the module
add a docstring for {fn} in the module
write a docstring at the start of {fn}
add a docstring to {fn} noting the owner
{fn}: add a docstring here noting the owner
{fn}: write a docstring as the first statement
{fn}: write a docstring now for new contributors
{fn}: attach a docstring first for new contributors
{fn}: attach a one-line docstring for new contributors
{fn}: write a one-line docstring for later maintainers
docstring added inside {fn} for the infrastructure team
{fn}: attach a one-line docstring for later maintainers
{fn}: docstring added first for the infrastructure team
add a new docstring at the start of {fn}
add a new docstring to {fn} in the module
{fn}: add a docstring to say what it does
{fn}: write a docstring to say what it does
add a docstring to {fn} to explain the intent
{fn}: add a new docstring now before the release
{fn}: write a docstring here to explain the intent
write a one-line docstring inside {fn} in the module
{fn}: add the missing docstring here for the reviewers
{fn}: insert a docstring here for the infrastructure team
{fn}: include a docstring first for the infrastructure team
{fn}: attach a one-line docstring first for later maintainers
{fn}: docstring added inside the function for new contributors
{fn}: docstring added inside the function for later maintainers
add a docstring to {fn} to say what it does
{fn}: add a new docstring to say what it does
add a docstring inside {fn} to say what it does
add a new docstring inside {fn} for the public API
{fn}: insert a docstring first so the intent is clear
write a one-line docstring to {fn} to explain the intent
{fn}: write a docstring for it for the infrastructure team
{fn}: docstring added as the first statement noting the owner
{fn}: add the missing docstring here for the infrastructure team
attach a one-line docstring inside {fn} for the infrastructure team
{fn}: attach a one-line docstring first for the infrastructure team
{fn}: docstring added inside the function for the infrastructure team
{fn}: add a docstring for it to say what it does
{fn}: insert a docstring for it to say what it does
{fn}: add a brief docstring for it for the public API
{fn}: add a one-line docstring for it for the public API
{fn}: add a brief docstring for it for the generated pages
attach a docstring at the start of {fn} for later maintainers
{fn}: insert a docstring to this function to explain the intent
{fn}: add the missing docstring to this function for the reviewers
{fn}: add the missing docstring to the function for new contributors
{fn}: attach a one-line docstring to this function for new contributors
{fn}: add a new docstring for it to say what it does
add a docstring at the start of {fn} for the public API
{fn}: write a one-line docstring to it to say what it does
{fn}: add a docstring to this function so the intent is clear
attach a docstring as the first statement of {fn} in the module
{fn}: add a brief docstring inside the function for the public API
{fn}: add a brief docstring to the function body for new contributors
{fn}: write a one-line docstring as the first statement noting the owner
docstring added right after the def of {fn} so the intent is clear
{fn}: add a docstring at the start of the function before the release
add the missing docstring right after the def of {fn} for the reviewers
{fn}: add a docstring right after the def line for the infrastructure team
{fn}: attach a one-line docstring inside the function so the intent is clear
{fn}: write a one-line docstring as the first statement for the generated pages
## doc N
write a docstring now
write a docstring here
include a docstring here
add the missing docstring
include a docstring first
write a one-line docstring
attach a one-line docstring
docstring added for readers
add a docstring to it
add a docstring for it
insert a docstring to it
add a brief docstring here
docstring added in the module
docstring added now for readers
docstring added before the release
docstring added inside the function
docstring added for new contributors
docstring added for later maintainers
add a new docstring to it
add a new docstring for it
add a brief docstring to it
add a brief docstring for it
add a one-line docstring to it
add the missing docstring for it
write a docstring first for readers
attach a docstring before the release
docstring added here before the release
docstring added now for later maintainers
docstring added first for later maintainers
docstring added for the infrastructure team
add a docstring now in the module
add a docstring to it for readers
add a new docstring in the module
add a docstring for the public API
add a docstring here in the module
add a new docstring to this function
add a brief docstring noting the owner
add a new docstring for new contributors
add a brief docstring for new contributors
docstring added here for the generated pages
write a one-line docstring for new contributors
docstring added here for the infrastructure team
attach a one-line docstring for later maintainers
docstring added first for the infrastructure team
add a docstring to it in the module
add a docstring to say what it does
add a docstring for it in the module
add a new docstring to it for readers
write a docstring to say what it does
attach a docstring for it in the module
insert a docstring to it noting the owner
write a docstring to it for new contributors
attach a one-line docstring for it for readers
add a one-line docstring first for the reviewers
attach a docstring now for the infrastructure team
attach a one-line docstring now for new contributors
attach a one-line docstring first for new contributors
docstring added inside the function for new contributors
add a new docstring to say what it does
add a docstring here to say what it does
write a docstring now to say what it does
write a docstring first to say what it does
add a new docstring first for the public API
insert a docstring here so the intent is clear
include a docstring here so the intent is clear
write a one-line docstring now for the public API
add a brief docstring to this function for readers
docstring added right after the def line for readers
write a one-line docstring here to explain the intent
docstring added to the function body before the release
docstring added to this function for the generated pages
docstring added to the function body for later maintainers
add a docstring to it to say what it does
add a docstring for it to say what it does
add a new docstring now to say what it does
attach a docstring for it to say what it does
insert a docstring to it so the intent is clear
add a one-line docstring for it for the public API
write a docstring to the function for the public API
write a one-line docstring first so the intent is clear
add a one-line docstring to the function noting the owner
docstring added to the function body for the generated pages
attach a one-line docstring to this function for the reviewers
add a one-line docstring inside the function for new contributors
add a brief docstring for it to say what it does
add a brief docstring for it so the intent is clear
write a one-line docstring for it to say what it does
docstring added to the function body to say what it does
insert a docstring to this function so the intent is clear
include a docstring right after the def line noting the owner
write a docstring right after the def line for new contributors
write a one-line docstring as the first statement noting the owner
add a one-line docstring to the function for the infrastructure team
attach a one-line docstring inside the function for the generated pages
add the missing docstring inside the function to say what it does
add a brief docstring to the function body for the generated pages
add the missing docstring inside the function so the intent is clear
add a one-line docstring to the function body for the generated pages
include a docstring at the start of the function for later maintainers
add a one-line docstring right after the def line for later maintainers
attach a one-line docstring right after the def line for new contributors
attach a one-line docstring as the first statement for the generated pages
add a one-line docstring right after the def line for the public API
write a docstring at the start of the function body for the reviewers
add a one-line docstring at the start of the function body for readers
attach a docstring at the start of the function body for the reviewers
attach a docstring at the start of the function for the generated pages
add the missing docstring right after the def line to explain the intent"""

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pools", "msg_messages.json")


def parse(src=SRC):
    """-> {kind: {"I": [text...], "N": [text...]}} in file order."""
    out, cur = {}, None
    for ln in src.strip("\n").split("\n"):
        if ln.startswith("## "):
            _h, kind, style = ln.split()
            cur = out.setdefault(kind, {}).setdefault(style, [])
        elif ln.strip():
            cur.append(ln.rstrip())
    return out


def main():
    from . import msg_pool as MP
    doc = MP.build_doc(parse())
    with open(OUT, "w", encoding="utf-8") as f:
        MP.dump(doc, f)
    print("wrote", OUT, {k: len(v["templates"]) for k, v in doc["kinds"].items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
