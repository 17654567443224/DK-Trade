package com.ruoyi.dk.quant.service.impl;

import java.util.Date;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.ruoyi.dk.quant.mapper.UpdatePlanMapper;
import com.ruoyi.dk.quant.mapper.UpdatePlanRecordMapper;
import com.ruoyi.dk.quant.domain.UpdatePlan;
import com.ruoyi.dk.quant.domain.UpdatePlanRecord;
import com.ruoyi.dk.quant.service.IUpdatePlanService;

/**
 * 更新计划 服务层实现
 */
@Service
public class UpdatePlanServiceImpl implements IUpdatePlanService {
    @Autowired
    private UpdatePlanMapper updatePlanMapper;

    @Autowired
    private UpdatePlanRecordMapper updatePlanRecordMapper;

    /**
     * 查询更新计划列表
     * 
     * @param updatePlan 更新计划信息
     * @return 更新计划集合
     */
    @Override
    public List<UpdatePlan> selectUpdatePlanList(UpdatePlan updatePlan) {
        return updatePlanMapper.selectUpdatePlanList(updatePlan);
    }

    /**
     * 查询更新计划总数
     * 
     * @param updatePlan 更新计划信息
     * @return 更新计划总数
     */
    @Override
    public int selectUpdatePlanCount(UpdatePlan updatePlan) {
        return updatePlanMapper.selectUpdatePlanCount(updatePlan);
    }

    /**
     * 查询更新计划详细信息
     * 
     * @param id 更新计划ID
     * @return 更新计划信息
     */
    @Override
    public UpdatePlan selectUpdatePlanById(Long id) {
        // 查询基本信息
        UpdatePlan updatePlan = updatePlanMapper.selectUpdatePlanById(id);
        if (updatePlan != null) {
            // 查询更新记录
            List<UpdatePlanRecord> records = updatePlanRecordMapper.selectUpdatePlanRecordsByPlanId(id);
            updatePlan.setUpdates(records);
        }
        return updatePlan;
    }

    /**
     * 新增更新计划
     * 
     * @param updatePlan 更新计划信息
     * @return 结果
     */
    @Override
    @Transactional
    public int insertUpdatePlan(UpdatePlan updatePlan) {
        // 设置发布日期为当前时间
        if (updatePlan.getCreateTime() == null) {
            updatePlan.setCreateTime(new Date());
        }
        
        // 设置更新时间
        updatePlan.setUpdateTime(new Date());
        
        // 插入更新计划
        return updatePlanMapper.insertUpdatePlan(updatePlan);
    }

    /**
     * 修改更新计划
     * 
     * @param updatePlan 更新计划信息
     * @return 结果
     */
    @Override
    @Transactional
    public int updateUpdatePlan(UpdatePlan updatePlan) {
        // 设置更新时间
        updatePlan.setUpdateTime(new Date());
        
        // 更新计划信息
        return updatePlanMapper.updateUpdatePlan(updatePlan);
    }

    /**
     * 删除更新计划对象
     * 
     * @param id 更新计划ID
     * @return 结果
     */
    @Override
    @Transactional
    public int deleteUpdatePlanById(Long id) {
        // 删除关联的更新记录
        updatePlanRecordMapper.deleteUpdatePlanRecordByPlanId(id);
        
        // 删除更新计划
        return updatePlanMapper.deleteUpdatePlanById(id);
    }

    /**
     * 批量删除更新计划信息
     * 
     * @param ids 需要删除的更新计划ID
     * @return 结果
     */
    @Override
    @Transactional
    public int deleteUpdatePlanByIds(Long[] ids) {
        // 删除关联的更新记录
        for (Long id : ids) {
            updatePlanRecordMapper.deleteUpdatePlanRecordByPlanId(id);
        }
        
        // 删除更新计划
        return updatePlanMapper.deleteUpdatePlanByIds(ids);
    }
} 