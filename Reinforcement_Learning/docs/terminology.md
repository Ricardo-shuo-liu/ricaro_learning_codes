state:
    状态：我认为是目标所处的环境信息（环境存在可观测和不可观测）
action:
    活动：我认为是目标可以实现的下一步活动
agent：
    智能体：所选目标
ploicy（pi）：
    策略：观测到agent的state选取action（作出决策）
    f(state) -> action
reward:
    奖励:激励或者用于调整ploicy
state transition
    状态转移:old state -> action ->new state
Return:
    Ut = Rt + Rt+1 + ...
    Ut(t时刻的return)
    Rt（t时刻的reward）
    Ut = Rt + gam*Rt+1 + gam^2 *Rt+1 ....
    gam<0,1>
