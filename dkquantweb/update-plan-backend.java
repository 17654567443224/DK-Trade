/**
 * 更新计划功能后端实现示例
 * 
 * 以下代码为Java Spring Boot实现，需要添加到后端项目中
 */

/**
 * 实体类定义
 */

// 更新计划实体类
package com.dkquant.system.domain;

import java.util.Date;
import java.util.List;

import javax.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "sys_update_plan")
public class UpdatePlan {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * 计划标题
     */
    private String title;
    
    /**
     * 计划描述
     */
    private String description;
    
    /**
     * 详细内容（富文本）
     */
    @Column(columnDefinition = "text")
    private String content;
    
    /**
     * 状态：planned-计划中，inProgress-进行中，completed-已完成
     */
    private String status;
    
    /**
     * 完成进度（百分比）
     */
    private Integer progress;
    
    /**
     * 预计完成日期
     */
    private Date dueDate;
    
    /**
     * 发布时间
     */
    private Date createTime;
    
    /**
     * 更新时间
     */
    private Date updateTime;
    
    /**
     * 创建者
     */
    private String createBy;
    
    /**
     * 更新者
     */
    private String updateBy;
    
    /**
     * 标签，以逗号分隔
     */
    private String tags;
    
    /**
     * 点赞数
     */
    private Integer likes;
    
    /**
     * 跟踪是否删除
     */
    private Integer delFlag;
}

// 更新记录实体类
package com.dkquant.system.domain;

import java.util.Date;

import javax.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "sys_update_record")
public class UpdateRecord {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * 关联的计划ID
     */
    private Long planId;
    
    /**
     * 更新内容
     */
    @Column(columnDefinition = "text")
    private String content;
    
    /**
     * 更新类型
     */
    private String type;
    
    /**
     * 更新时间
     */
    private Date updateTime;
    
    /**
     * 创建者
     */
    private String createBy;
    
    /**
     * 删除标记
     */
    private Integer delFlag;
}

// 用户点赞记录实体类
package com.dkquant.system.domain;

import java.util.Date;

import javax.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "sys_update_plan_like")
public class UpdatePlanLike {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * 用户ID
     */
    private Long userId;
    
    /**
     * 计划ID
     */
    private Long planId;
    
    /**
     * 点赞时间
     */
    private Date createTime;
}

/**
 * 数据传输对象 (DTO)
 */
package com.dkquant.system.dto;

import java.util.Date;
import java.util.List;
import lombok.Data;

@Data
public class UpdatePlanDTO {
    private Long id;
    private String title;
    private String description;
    private String content;
    private String status;
    private Integer progress;
    private Date dueDate;
    private Date createTime;
    private Date updateTime;
    private List<String> tags;
    private Integer likes;
    private Boolean isLiked;
    private List<UpdateRecordDTO> updates;
}

@Data
public class UpdateRecordDTO {
    private Long id;
    private Long planId;
    private String content;
    private String type;
    private Date updateTime;
}

/**
 * 存储库接口
 */
package com.dkquant.system.repository;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import com.dkquant.system.domain.UpdatePlan;

@Repository
public interface UpdatePlanRepository extends JpaRepository<UpdatePlan, Long> {
    
    List<UpdatePlan> findByStatusAndDelFlagOrderByCreateTimeDesc(String status, Integer delFlag);
    
    @Query("SELECT p FROM UpdatePlan p WHERE p.delFlag = 0 AND " +
           "(p.title LIKE %?1% OR p.description LIKE %?1% OR p.tags LIKE %?1%) " +
           "ORDER BY p.createTime DESC")
    List<UpdatePlan> searchByKeyword(String keyword);
    
    @Query("SELECT p FROM UpdatePlan p WHERE p.delFlag = 0 ORDER BY p.likes DESC")
    List<UpdatePlan> findAllOrderByLikes();
    
    @Query("SELECT p FROM UpdatePlan p WHERE p.delFlag = 0 ORDER BY p.dueDate ASC")
    List<UpdatePlan> findAllOrderByDueDate();
}

@Repository
public interface UpdateRecordRepository extends JpaRepository<UpdateRecord, Long> {
    
    List<UpdateRecord> findByPlanIdAndDelFlagOrderByUpdateTimeDesc(Long planId, Integer delFlag);
}

@Repository
public interface UpdatePlanLikeRepository extends JpaRepository<UpdatePlanLike, Long> {
    
    boolean existsByUserIdAndPlanId(Long userId, Long planId);
    
    void deleteByUserIdAndPlanId(Long userId, Long planId);
}

/**
 * 服务接口和实现
 */
package com.dkquant.system.service;

import java.util.List;
import com.dkquant.system.dto.UpdatePlanDTO;
import com.dkquant.common.core.domain.AjaxResult;

public interface IUpdatePlanService {
    
    /**
     * 获取更新计划列表
     */
    AjaxResult list(String status, Integer pageNum, Integer pageSize, String sort, String keyword);
    
    /**
     * 获取更新计划详情
     */
    AjaxResult getInfo(Long id);
    
    /**
     * 添加更新计划
     */
    AjaxResult add(UpdatePlanDTO updatePlan);
    
    /**
     * 修改更新计划
     */
    AjaxResult update(UpdatePlanDTO updatePlan);
    
    /**
     * 删除更新计划
     */
    AjaxResult delete(Long id);
    
    /**
     * 切换点赞状态
     */
    AjaxResult toggleLike(Long id, Long userId);
    
    /**
     * 添加更新记录
     */
    AjaxResult addRecord(Long planId, String content, String type);
}

package com.dkquant.system.service.impl;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.dkquant.common.core.domain.AjaxResult;
import com.dkquant.common.utils.SecurityUtils;
import com.dkquant.common.utils.StringUtils;
import com.dkquant.system.domain.UpdatePlan;
import com.dkquant.system.domain.UpdateRecord;
import com.dkquant.system.domain.UpdatePlanLike;
import com.dkquant.system.dto.UpdatePlanDTO;
import com.dkquant.system.dto.UpdateRecordDTO;
import com.dkquant.system.repository.UpdatePlanRepository;
import com.dkquant.system.repository.UpdateRecordRepository;
import com.dkquant.system.repository.UpdatePlanLikeRepository;
import com.dkquant.system.service.IUpdatePlanService;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;

@Service
public class UpdatePlanServiceImpl implements IUpdatePlanService {

    @Autowired
    private UpdatePlanRepository updatePlanRepository;
    
    @Autowired
    private UpdateRecordRepository updateRecordRepository;
    
    @Autowired
    private UpdatePlanLikeRepository updatePlanLikeRepository;
    
    @Override
    public AjaxResult list(String status, Integer pageNum, Integer pageSize, String sort, String keyword) {
        List<UpdatePlan> updatePlans;
        
        PageHelper.startPage(pageNum, pageSize);
        
        // 根据参数获取列表
        if (StringUtils.isNotEmpty(keyword)) {
            updatePlans = updatePlanRepository.searchByKeyword(keyword);
        } else if (StringUtils.isNotEmpty(status)) {
            updatePlans = updatePlanRepository.findByStatusAndDelFlagOrderByCreateTimeDesc(status, 0);
        } else if ("likes".equals(sort)) {
            updatePlans = updatePlanRepository.findAllOrderByLikes();
        } else if ("dueDate".equals(sort)) {
            updatePlans = updatePlanRepository.findAllOrderByDueDate();
        } else {
            updatePlans = updatePlanRepository.findAll();
        }
        
        PageInfo<UpdatePlan> pageInfo = new PageInfo<>(updatePlans);
        
        // 转换为DTO列表
        List<UpdatePlanDTO> dtoList = new ArrayList<>();
        Long currentUserId = SecurityUtils.getCurrentUserId();
        
        for (UpdatePlan plan : updatePlans) {
            UpdatePlanDTO dto = new UpdatePlanDTO();
            BeanUtils.copyProperties(plan, dto);
            
            // 处理标签
            if (StringUtils.isNotEmpty(plan.getTags())) {
                dto.setTags(Arrays.asList(plan.getTags().split(",")));
            }
            
            // 判断当前用户是否已点赞
            if (currentUserId != null) {
                dto.setIsLiked(updatePlanLikeRepository.existsByUserIdAndPlanId(currentUserId, plan.getId()));
            } else {
                dto.setIsLiked(false);
            }
            
            dtoList.add(dto);
        }
        
        return AjaxResult.success(dtoList, pageInfo.getTotal());
    }
    
    @Override
    public AjaxResult getInfo(Long id) {
        UpdatePlan updatePlan = updatePlanRepository.findById(id).orElse(null);
        if (updatePlan == null) {
            return AjaxResult.error("更新计划不存在");
        }
        
        UpdatePlanDTO dto = new UpdatePlanDTO();
        BeanUtils.copyProperties(updatePlan, dto);
        
        // 处理标签
        if (StringUtils.isNotEmpty(updatePlan.getTags())) {
            dto.setTags(Arrays.asList(updatePlan.getTags().split(",")));
        }
        
        // 获取更新记录
        List<UpdateRecord> records = updateRecordRepository.findByPlanIdAndDelFlagOrderByUpdateTimeDesc(id, 0);
        List<UpdateRecordDTO> recordDtos = records.stream().map(record -> {
            UpdateRecordDTO recordDto = new UpdateRecordDTO();
            BeanUtils.copyProperties(record, recordDto);
            return recordDto;
        }).collect(Collectors.toList());
        dto.setUpdates(recordDtos);
        
        // 判断当前用户是否已点赞
        Long currentUserId = SecurityUtils.getCurrentUserId();
        if (currentUserId != null) {
            dto.setIsLiked(updatePlanLikeRepository.existsByUserIdAndPlanId(currentUserId, id));
        } else {
            dto.setIsLiked(false);
        }
        
        return AjaxResult.success(dto);
    }
    
    @Override
    @Transactional
    public AjaxResult add(UpdatePlanDTO updatePlanDto) {
        UpdatePlan updatePlan = new UpdatePlan();
        BeanUtils.copyProperties(updatePlanDto, updatePlan);
        
        // 设置创建信息
        updatePlan.setCreateTime(new Date());
        updatePlan.setCreateBy(SecurityUtils.getUsername());
        updatePlan.setDelFlag(0);
        updatePlan.setLikes(0);
        
        // 处理标签
        if (updatePlanDto.getTags() != null && !updatePlanDto.getTags().isEmpty()) {
            updatePlan.setTags(String.join(",", updatePlanDto.getTags()));
        }
        
        updatePlanRepository.save(updatePlan);
        
        return AjaxResult.success("添加成功");
    }
    
    @Override
    @Transactional
    public AjaxResult update(UpdatePlanDTO updatePlanDto) {
        UpdatePlan existing = updatePlanRepository.findById(updatePlanDto.getId()).orElse(null);
        if (existing == null) {
            return AjaxResult.error("更新计划不存在");
        }
        
        BeanUtils.copyProperties(updatePlanDto, existing);
        
        // 设置更新信息
        existing.setUpdateTime(new Date());
        existing.setUpdateBy(SecurityUtils.getUsername());
        
        // 处理标签
        if (updatePlanDto.getTags() != null && !updatePlanDto.getTags().isEmpty()) {
            existing.setTags(String.join(",", updatePlanDto.getTags()));
        }
        
        updatePlanRepository.save(existing);
        
        // 添加更新记录
        addRecord(updatePlanDto.getId(), "计划已更新", "update");
        
        return AjaxResult.success("修改成功");
    }
    
    @Override
    @Transactional
    public AjaxResult delete(Long id) {
        UpdatePlan updatePlan = updatePlanRepository.findById(id).orElse(null);
        if (updatePlan == null) {
            return AjaxResult.error("更新计划不存在");
        }
        
        // 逻辑删除
        updatePlan.setDelFlag(1);
        updatePlanRepository.save(updatePlan);
        
        return AjaxResult.success("删除成功");
    }
    
    @Override
    @Transactional
    public AjaxResult toggleLike(Long id, Long userId) {
        UpdatePlan updatePlan = updatePlanRepository.findById(id).orElse(null);
        if (updatePlan == null) {
            return AjaxResult.error("更新计划不存在");
        }
        
        // 判断是点赞还是取消点赞
        boolean exists = updatePlanLikeRepository.existsByUserIdAndPlanId(userId, id);
        
        if (exists) {
            // 取消点赞
            updatePlanLikeRepository.deleteByUserIdAndPlanId(userId, id);
            updatePlan.setLikes(updatePlan.getLikes() - 1);
            updatePlanRepository.save(updatePlan);
            return AjaxResult.success("取消点赞成功");
        } else {
            // 添加点赞
            UpdatePlanLike like = new UpdatePlanLike();
            like.setUserId(userId);
            like.setPlanId(id);
            like.setCreateTime(new Date());
            updatePlanLikeRepository.save(like);
            
            updatePlan.setLikes(updatePlan.getLikes() + 1);
            updatePlanRepository.save(updatePlan);
            return AjaxResult.success("点赞成功");
        }
    }
    
    @Override
    @Transactional
    public AjaxResult addRecord(Long planId, String content, String type) {
        UpdatePlan updatePlan = updatePlanRepository.findById(planId).orElse(null);
        if (updatePlan == null) {
            return AjaxResult.error("更新计划不存在");
        }
        
        UpdateRecord record = new UpdateRecord();
        record.setPlanId(planId);
        record.setContent(content);
        record.setType(type);
        record.setUpdateTime(new Date());
        record.setCreateBy(SecurityUtils.getUsername());
        record.setDelFlag(0);
        
        updateRecordRepository.save(record);
        
        return AjaxResult.success("添加更新记录成功");
    }
}

/**
 * 控制器
 */
package com.dkquant.web.controller.system;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.dkquant.common.core.domain.AjaxResult;
import com.dkquant.common.utils.SecurityUtils;
import com.dkquant.system.dto.UpdatePlanDTO;
import com.dkquant.system.dto.UpdateRecordDTO;
import com.dkquant.system.service.IUpdatePlanService;

@RestController
@RequestMapping("/system/updatePlan")
public class UpdatePlanController {
    
    @Autowired
    private IUpdatePlanService updatePlanService;
    
    /**
     * 获取更新计划列表
     */
    @GetMapping("/list")
    public AjaxResult list(
            @RequestParam(required = false) String status,
            @RequestParam(required = false, defaultValue = "1") Integer page,
            @RequestParam(required = false, defaultValue = "10") Integer pageSize,
            @RequestParam(required = false) String sort,
            @RequestParam(required = false) String keyword) {
        
        return updatePlanService.list(status, page, pageSize, sort, keyword);
    }
    
    /**
     * 获取更新计划详情
     */
    @GetMapping("/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id) {
        return updatePlanService.getInfo(id);
    }
    
    /**
     * 添加更新计划
     */
    @PostMapping
    @PreAuthorize("@ss.hasPermi('system:updatePlan:add')")
    public AjaxResult add(@RequestBody UpdatePlanDTO updatePlan) {
        return updatePlanService.add(updatePlan);
    }
    
    /**
     * 修改更新计划
     */
    @PutMapping
    @PreAuthorize("@ss.hasPermi('system:updatePlan:edit')")
    public AjaxResult edit(@RequestBody UpdatePlanDTO updatePlan) {
        return updatePlanService.update(updatePlan);
    }
    
    /**
     * 删除更新计划
     */
    @DeleteMapping("/{id}")
    @PreAuthorize("@ss.hasPermi('system:updatePlan:delete')")
    public AjaxResult delete(@PathVariable("id") Long id) {
        return updatePlanService.delete(id);
    }
    
    /**
     * 切换点赞状态
     */
    @PostMapping("/like/{id}")
    public AjaxResult toggleLike(@PathVariable("id") Long id) {
        Long userId = SecurityUtils.getCurrentUserId();
        if (userId == null) {
            return AjaxResult.error("请先登录");
        }
        return updatePlanService.toggleLike(id, userId);
    }
    
    /**
     * 添加更新记录
     */
    @PostMapping("/record")
    @PreAuthorize("@ss.hasPermi('system:updatePlan:addRecord')")
    public AjaxResult addRecord(@RequestBody UpdateRecordDTO record) {
        return updatePlanService.addRecord(record.getPlanId(), record.getContent(), record.getType());
    }
}

/**
 * 数据库表结构
 * 
 * 1. 更新计划表 (sys_update_plan)
 * +-------------+--------------+------+-----+---------+----------------+
 * | Field       | Type         | Null | Key | Default | Extra          |
 * +-------------+--------------+------+-----+---------+----------------+
 * | id          | bigint(20)   | NO   | PRI | NULL    | auto_increment |
 * | title       | varchar(100) | NO   |     | NULL    |                |
 * | description | varchar(500) | YES  |     | NULL    |                |
 * | content     | text         | YES  |     | NULL    |                |
 * | status      | varchar(20)  | NO   |     | NULL    |                |
 * | progress    | int(11)      | NO   |     | 0       |                |
 * | due_date    | datetime     | YES  |     | NULL    |                |
 * | create_time | datetime     | NO   |     | NULL    |                |
 * | update_time | datetime     | YES  |     | NULL    |                |
 * | create_by   | varchar(50)  | YES  |     | NULL    |                |
 * | update_by   | varchar(50)  | YES  |     | NULL    |                |
 * | tags        | varchar(200) | YES  |     | NULL    |                |
 * | likes       | int(11)      | NO   |     | 0       |                |
 * | del_flag    | tinyint(4)   | NO   |     | 0       |                |
 * +-------------+--------------+------+-----+---------+----------------+
 * 
 * 2. 更新记录表 (sys_update_record)
 * +-------------+--------------+------+-----+---------+----------------+
 * | Field       | Type         | Null | Key | Default | Extra          |
 * +-------------+--------------+------+-----+---------+----------------+
 * | id          | bigint(20)   | NO   | PRI | NULL    | auto_increment |
 * | plan_id     | bigint(20)   | NO   | MUL | NULL    |                |
 * | content     | text         | NO   |     | NULL    |                |
 * | type        | varchar(20)  | YES  |     | NULL    |                |
 * | update_time | datetime     | NO   |     | NULL    |                |
 * | create_by   | varchar(50)  | YES  |     | NULL    |                |
 * | del_flag    | tinyint(4)   | NO   |     | 0       |                |
 * +-------------+--------------+------+-----+---------+----------------+
 * 
 * 3. 用户点赞表 (sys_update_plan_like)
 * +-------------+------------+------+-----+---------+----------------+
 * | Field       | Type       | Null | Key | Default | Extra          |
 * +-------------+------------+------+-----+---------+----------------+
 * | id          | bigint(20) | NO   | PRI | NULL    | auto_increment |
 * | user_id     | bigint(20) | NO   | MUL | NULL    |                |
 * | plan_id     | bigint(20) | NO   | MUL | NULL    |                |
 * | create_time | datetime   | NO   |     | NULL    |                |
 * +-------------+------------+------+-----+---------+----------------+
 */ 