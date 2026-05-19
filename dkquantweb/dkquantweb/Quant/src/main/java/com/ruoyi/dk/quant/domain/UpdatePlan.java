package com.ruoyi.dk.quant.domain;

import java.util.Date;
import java.util.List;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

/**
 * 更新计划对象 update_plan
 */
public class UpdatePlan {
    private static final long serialVersionUID = 1L;

    /** 主键ID */
    private Long id;

    /** 计划标题 */
    private String title;

    /** 计划描述 */
    private String description;

    /** 详细内容 */
    private String content;

    /** 状态：planned-计划中, inProgress-进行中, completed-已完成 */
    private String status;

    /** 完成进度（百分比） */
    private Integer progress;

    /** 发布日期 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date createTime;

    /** 预计完成日期 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date dueDate;

    /** 相关标签，逗号分隔 */
    private String tags;

    /** 创建者 */
    private String createBy;

    /** 更新者 */
    private String updateBy;

    /** 更新时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date updateTime;
    
    /** 相关标签列表 */
    private String[] tagList;
    
    /** 更新记录列表 */
    private List<UpdatePlanRecord> updates;
    
    /** 排序方式 */
    private String sort;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Integer getProgress() {
        return progress;
    }

    public void setProgress(Integer progress) {
        this.progress = progress;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public Date getDueDate() {
        return dueDate;
    }

    public void setDueDate(Date dueDate) {
        this.dueDate = dueDate;
    }

    public String getTags() {
        return tags;
    }

    public void setTags(String tags) {
        this.tags = tags;
    }

    public String getCreateBy() {
        return createBy;
    }

    public void setCreateBy(String createBy) {
        this.createBy = createBy;
    }

    public String getUpdateBy() {
        return updateBy;
    }

    public void setUpdateBy(String updateBy) {
        this.updateBy = updateBy;
    }

    public Date getUpdateTime() {
        return updateTime;
    }

    public void setUpdateTime(Date updateTime) {
        this.updateTime = updateTime;
    }
    
    public String[] getTagList() {
        if (tags != null && !tags.isEmpty()) {
            return tags.split(",");
        }
        return new String[0];
    }

    public void setTagList(String[] tagList) {
        this.tagList = tagList;
    }
    
    public List<UpdatePlanRecord> getUpdates() {
        return updates;
    }

    public void setUpdates(List<UpdatePlanRecord> updates) {
        this.updates = updates;
    }

    public String getSort() {
        return sort;
    }

    public void setSort(String sort) {
        this.sort = sort;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this, ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("title", getTitle())
            .append("description", getDescription())
            .append("content", getContent())
            .append("status", getStatus())
            .append("progress", getProgress())
            .append("createTime", getCreateTime())
            .append("dueDate", getDueDate())
            .append("tags", getTags())
            .append("createBy", getCreateBy())
            .append("updateBy", getUpdateBy())
            .append("updateTime", getUpdateTime())
            .toString();
    }
} 