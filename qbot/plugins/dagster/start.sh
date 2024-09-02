###
# @Author: Charmve yidazhang1@gmail.com
# @Date: 2023-03-26 00:56:57
# @LastEditors: Charmve yidazhang1@gmail.com
# @LastEditTime: 2023-03-26 00:58:07
# @FilePath: /Qbot/dagster/start.sh
# @Version: 1.0.1
# @Blogs: charmve.blog.csdn.net
# @GitHub: https://github.com/Charmve
# @Description:
#
# Copyright (c) 2023 by Charmve, All Rights Reserved.
# Licensed under the MIT License.
###

dagster-daemon run &
dagit -h 0.0.0.0 -p 3000
