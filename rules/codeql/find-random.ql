/**
 * @name Math.random finder
 * @kind problem
 * @problem.severity error
 * @id arcblroth/ece117-unpredictables/find-random
 */

import javascript

class MathRandomTaintConfig extends TaintTracking::Configuration {
  MathRandomTaintConfig() { this = "MathRandomTaintConfig" }

  override predicate isSource(DataFlow::Node source) {
    DataFlow::globalVarRef("Math").getAPropertyRead("random").getACall() = source
  }

  override predicate isSink(DataFlow::Node sink) {
    sink instanceof Http::ResponseSendArgument
    or
    DataFlow::globalVarRef("Response").getAnInstantiation().getAnArgument() = sink
  }

  override predicate isAdditionalTaintStep(DataFlow::Node pred, DataFlow::Node succ) {
    succ.asExpr().(Expr).getAChildExpr() = pred.asExpr()
  }
}

from MathRandomTaintConfig cfg, DataFlow::Node source, DataFlow::Node sink
where cfg.hasFlow(source, sink)
select sink, "Math.random exposed to user from $@.", source, "here"
