package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.UpdatePlanRecord;

/**
 * 更新计划记录 Mapper接口
 */
public interface UpdatePlanRecordMapper {
    /**
     * 查询更新计划记录列表
     *
     * @param updatePlanRecord 更新计划记录信息
     * @return 更新计划记录集合
     */
    public List<UpdatePlanRecord> selectUpdatePlanRecordList(UpdatePlanRecord updatePlanRecord);

    /**
     * 根据计划ID查询更新记录
     *
     * @param planId 计划ID
     * @return 更新记录集合
     */
    public List<UpdatePlanRecord> selectUpdatePlanRecordsByPlanId(Long planId);

    /**
     * 查询更新记录详细信息
     *
     * @param id 更新记录ID
     * @return 更新记录信息
     */
    public UpdatePlanRecord selectUpdatePlanRecordById(Long id);

    /**
     * 新增更新记录
     *
     * @param updatePlanRecord 更新记录信息
     * @return 结果
     */
    public int insertUpdatePlanRecord(UpdatePlanRecord updatePlanRecord);

    /**
     * 修改更新记录
     *
     * @param updatePlanRecord 更新记录信息
     * @return 结果
     */
    public int updateUpdatePlanRecord(UpdatePlanRecord updatePlanRecord);

    /**
     * 删除更新记录
     *
     * @param id 更新记录ID
     * @return 结果
     */
    public int deleteUpdatePlanRecordById(Long id);

    /**
     * 批量删除更新记录
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteUpdatePlanRecordByIds(Long[] ids);

    /**
     * 根据计划ID删除更新记录
     *
     * @param planId 计划ID
     * @return 结果
     */
    public int deleteUpdatePlanRecordByPlanId(Long planId);
} 