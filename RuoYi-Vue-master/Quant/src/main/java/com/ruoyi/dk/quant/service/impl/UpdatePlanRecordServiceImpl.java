package com.ruoyi.dk.quant.service.impl;

import java.util.Date;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.UpdatePlanRecordMapper;
import com.ruoyi.dk.quant.domain.UpdatePlanRecord;
import com.ruoyi.dk.quant.service.IUpdatePlanRecordService;

/**
 * 更新计划记录 服务层实现
 */
@Service
public class UpdatePlanRecordServiceImpl implements IUpdatePlanRecordService {
    @Autowired
    private UpdatePlanRecordMapper updatePlanRecordMapper;

    /**
     * 查询更新计划记录列表
     * 
     * @param updatePlanRecord 更新计划记录信息
     * @return 更新计划记录集合
     */
    @Override
    public List<UpdatePlanRecord> selectUpdatePlanRecordList(UpdatePlanRecord updatePlanRecord) {
        return updatePlanRecordMapper.selectUpdatePlanRecordList(updatePlanRecord);
    }

    /**
     * 根据计划ID查询更新记录
     * 
     * @param planId 计划ID
     * @return 更新记录集合
     */
    @Override
    public List<UpdatePlanRecord> selectUpdatePlanRecordsByPlanId(Long planId) {
        return updatePlanRecordMapper.selectUpdatePlanRecordsByPlanId(planId);
    }

    /**
     * 查询更新记录详细信息
     * 
     * @param id 更新记录ID
     * @return 更新记录信息
     */
    @Override
    public UpdatePlanRecord selectUpdatePlanRecordById(Long id) {
        return updatePlanRecordMapper.selectUpdatePlanRecordById(id);
    }

    /**
     * 新增更新记录
     * 
     * @param updatePlanRecord 更新记录信息
     * @return 结果
     */
    @Override
    public int insertUpdatePlanRecord(UpdatePlanRecord updatePlanRecord) {
        // 设置更新时间为当前时间
        if (updatePlanRecord.getUpdateTime() == null) {
            updatePlanRecord.setUpdateTime(new Date());
        }
        
        // 设置默认类型
        if (updatePlanRecord.getType() == null) {
            updatePlanRecord.setType("primary");
        }
        
        return updatePlanRecordMapper.insertUpdatePlanRecord(updatePlanRecord);
    }

    /**
     * 修改更新记录
     * 
     * @param updatePlanRecord 更新记录信息
     * @return 结果
     */
    @Override
    public int updateUpdatePlanRecord(UpdatePlanRecord updatePlanRecord) {
        // 设置更新时间为当前时间
        updatePlanRecord.setUpdateTime(new Date());
        
        return updatePlanRecordMapper.updateUpdatePlanRecord(updatePlanRecord);
    }

    /**
     * 删除更新记录对象
     * 
     * @param id 更新记录ID
     * @return 结果
     */
    @Override
    public int deleteUpdatePlanRecordById(Long id) {
        return updatePlanRecordMapper.deleteUpdatePlanRecordById(id);
    }

    /**
     * 批量删除更新记录信息
     * 
     * @param ids 需要删除的更新记录ID
     * @return 结果
     */
    @Override
    public int deleteUpdatePlanRecordByIds(Long[] ids) {
        return updatePlanRecordMapper.deleteUpdatePlanRecordByIds(ids);
    }

    /**
     * 根据计划ID删除更新记录
     * 
     * @param planId 计划ID
     * @return 结果
     */
    @Override
    public int deleteUpdatePlanRecordByPlanId(Long planId) {
        return updatePlanRecordMapper.deleteUpdatePlanRecordByPlanId(planId);
    }
} 