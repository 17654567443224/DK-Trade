package com.ruoyi.dk.quant.service;

import java.util.List;
import com.ruoyi.dk.quant.domain.UpdatePlan;

/**
 * 更新计划服务接口
 */
public interface IUpdatePlanService {
    /**
     * 查询更新计划列表
     *
     * @param updatePlan 更新计划信息
     * @return 更新计划集合
     */
    public List<UpdatePlan> selectUpdatePlanList(UpdatePlan updatePlan);

    /**
     * 查询更新计划总数
     *
     * @param updatePlan 更新计划信息
     * @return 更新计划总数
     */
    public int selectUpdatePlanCount(UpdatePlan updatePlan);

    /**
     * 查询更新计划详细信息
     *
     * @param id 更新计划ID
     * @return 更新计划信息
     */
    public UpdatePlan selectUpdatePlanById(Long id);

    /**
     * 新增更新计划
     *
     * @param updatePlan 更新计划信息
     * @return 结果
     */
    public int insertUpdatePlan(UpdatePlan updatePlan);

    /**
     * 修改更新计划
     *
     * @param updatePlan 更新计划信息
     * @return 结果
     */
    public int updateUpdatePlan(UpdatePlan updatePlan);

    /**
     * 删除更新计划信息
     *
     * @param id 更新计划ID
     * @return 结果
     */
    public int deleteUpdatePlanById(Long id);

    /**
     * 批量删除更新计划信息
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteUpdatePlanByIds(Long[] ids);
} 