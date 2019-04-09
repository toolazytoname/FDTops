#1.category 的重命名
#2.category 里面的方法重命名
#3.宏 的方法重命名
#3.加入词法分析，语法分析树的逻辑
#4.加入了词法树以后，可以看当前类依赖了哪些别的类，列出来
#5.tops里面可以手动加一些代码
#6.tops工具有很多玩法，继续看看man






# coding=utf-8
import os
import sys

def obtan_dir_names(work_dir):
    '''

    :param work_dir: 目标目录
    :return:return:根据文件目录集合生成一个字符串
    '''
    parent_set = set()
    for parent, dirnames, filenames in os.walk(work_dir):
        #  filenames.__len__() > 0 避免文件夹下面没有文件
        if parent.endswith('/') and filenames.__len__() > 0:
            parent_set.add('{0}*'.format(parent))
        elif filenames.__len__() > 0:
            parent_set.add('{0}/*'.format(parent))
    parent_string = ' '.join(str(parent) for parent in parent_set)
    return parent_string


def obtain_class_name_set(work_dir):
    '''
    获取代操作类名的集合
    :param work_dir:目标目录
    :return:  获取代操作类名的集合
    '''
    class_name_set = set()
    for parent, dirnames, filenames in os.walk(work_dir):
        for filename in filenames:
            # 有的时候文件夹内只有xib文件，所以加上这个条件
            # 发现有的文件只有.m，所以加上.m，考虑是否要和obtain_file_path_set 中的条件统一
            if filename.endswith('.h') or filename.endswith('.m') or filename.endswith('.xib'):
                (shortname, extension) = os.path.splitext(filename)
                class_name_set.add(shortname)
    return class_name_set

def obtain_class_rename_dic(operation, prefix, des_prefix, class_name_set):
    '''
    获取一个字典，key为原始类名，value 为目标类名
    :param operation:操作符，目前支持 replace  和 add
    :param prefix: 前缀
    :param des_prefix:替换的目标前缀
    :param class_name_set: 类名集合
    :return: 一个字典，key为原始类名，value 为目标类名
    '''
    class_rename_dic = dict()
    for class_name in class_name_set:
        if 'add' == operation:
            class_rename_dic[class_name] = '{0}{1}'.format(prefix, class_name)
        elif 'replace' == operation:
            class_rename_dic[class_name] = class_name.replace(prefix, des_prefix)
    return class_rename_dic


def save_tops_file(work_dir, class_rename_dic):
    '''
    以传入的目标目录名为文件名，维护一个tops替换规则文件
    :param work_dir:工作目录
    :param operation: 操作符，分add 和 replace 两种
    :param prefix: 前缀
    :return:  以传入的目标目录名为文件名，维护一个tops替换规则文件
    '''
    (work_dir_dirname, work_dir_filename) = os.path.split(work_dir)
    tops_line_set = set()
    # for class_name, des_class_name in class_rename_dic.items():
    tops_line_set = {'replace "{0}" with "{1}"'.format(key, value)for key, value in class_rename_dic.items()}

    # print('tops_line_set is {0}'.format(tops_line_set))
    # print('work_dir_dirname is {0}'.format(work_dir_filename))
    with open('{0}.tops'.format(work_dir_filename), mode='w', encoding='utf-8') as a_file:
        for tops_line in tops_line_set:
            a_file.writelines(tops_line)
            a_file.write('\n')


def run_shell(work_dir, parentString):
    '''
    根据传入的参数执行tops 命令行工具
    :param work_dir:目标目录
    :param parentString: 目标目录
    :return:
    '''
    (work_dir_dirname, work_dir_filename) = os.path.split(work_dir)
    shellString = 'tops -semiverbose -scriptfile ./{0}.tops  {1}'.format(work_dir_filename, parentString)
    print('shellString:{0}'.format(shellString))
    os.system(shellString)

def obtain_file_path_set(work_dir):
    '''
    获取待操作文件的集合
    :param work_dir:目标目录
    :return: 待操作文件集合
    '''
    file_path_set = set()
    for parent, dirnames, filenames in os.walk(work_dir):
        for filename in filenames:
            if filename.endswith('.h') or filename.endswith('.m') or filename.endswith('.xib'):
                file_path = os.path.join(parent, filename)
                file_path_set.add(file_path)
    return file_path_set


def rename_class_handle(class_rename_dic, file_path_set):
    '''
    手动操作文件中的内容

    :param class_rename_dic:
    :param file_path_set:
    :return:
    '''
    for file_path in file_path_set:
        with open(file_path, "r+") as file:
            read_data = file.read()
            file.seek(0, 0)
            for key, value in class_rename_dic.items():
                # 此处可以增加一个循环
                original_string = '"{0}.h"'.format(key)
                des_string = '"{0}.h"'.format(value)
                read_data = read_data.replace(original_string, des_string)
                original_string = '"{0}"'.format(key)
                des_string = '"{0}"'.format(value)
                read_data = read_data.replace(original_string, des_string)
                # 为了兼顾，/YCHomePageHeaderView" owner:self options:nil].firstObject;这种场景
                original_string = '/{0}"'.format(key)
                des_string = '/{0}"'.format(value)
                read_data = read_data.replace(original_string, des_string)
            file.write(read_data)

def obtain_filepath_dic(class_rename_dic, file_path_set):
    '''
    返回 原始文件名 和 目标文件名 映射的字典
    :param class_rename_dic:原始类，目标类名映射关系的字典
    :param file_path_set:原始文件名的集合
    :return:返回key为原始文件名，value为目标文件名 映射的字典
    '''
    file_path_dic = dict()
    for file_path in file_path_set:
        (file_path_dirname, file_path_fileName) = os.path.split(file_path)
        (shortname, extension) = os.path.splitext(file_path_fileName)
        if class_rename_dic.__contains__(shortname):
            new_file_name = '{0}{1}'.format(class_rename_dic[shortname], extension)
            new_file_path = os.path.join(file_path_dirname, new_file_name)
            file_path_dic[file_path] = new_file_path
    return file_path_dic

def os_rename(file_path_dic):
    '''
    批量重命名文件
    :param file_path_dic:key为原始文件名，value为目标文件名
    :return:
    '''
    {os.rename(oldFilePath, newFilePath) for oldFilePath, newFilePath in file_path_dic.items()}



if __name__=='__main__':
    work_dir = sys.argv[1]
    operation = sys.argv[2]
    prefix = sys.argv[3]
    des_prefix = ''
    if sys.argv.__len__() >= 5:
        des_prefix = sys.argv[4]

    dir_names = obtan_dir_names(work_dir)
    class_name_set = obtain_class_name_set(work_dir)
    class_rename_dic = obtain_class_rename_dic(operation, prefix, des_prefix, class_name_set)
    save_tops_file(work_dir, class_rename_dic)
    if class_name_set.__len__() > 0:
        run_shell(work_dir, dir_names)

    file_path_set = obtain_file_path_set(work_dir)
    file_path_dic = obtain_filepath_dic(class_rename_dic, file_path_set)
    rename_class_handle(class_rename_dic,file_path_set)

    os_rename(file_path_dic)
